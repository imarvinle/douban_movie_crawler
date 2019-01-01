#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from app import db, app
from app.models.model import Tag
from app.models.model import Movie
from app.models.model import Language, Country
from flask import jsonify, request
from functools import reduce


@app.route("/movie/tag")
def tag_num_list():
    threshold = 20
    data = []
    tags = Tag.query.all()
    tags = list(map(lambda x : {"value": x.num, "name": x.name}, tags))
    tags = sorted(tags, key=lambda x : x["value"], reverse=True)
    if len(tags) > threshold:
        data.extend(tags[0:threshold])
        other_num = reduce(lambda x, y: x + y, map(lambda x: x["value"], tags[threshold:-1]))
        data.append({"name": "其它", "value": other_num})
    else:
        data = tags

    return jsonify({"data": data})



@app.route("/movie/director")
def director_movies_num():
    data = []
    directors = db.session.query(Movie.director, db.func.count('*').label('director_group')).group_by(Movie.director).all()
    new_directors = []
    for director in directors:
        if director[0] != "" and director[0] != " ":
            new_directors.append(director)
    directors = sorted(new_directors, key=lambda x: x[1],  reverse=True)[0:10]
    for director in directors:
        data.append({'value': director[1], 'name': director[0]})
    return jsonify({'data': data})


@app.route("/movie/language")
def language_static():
    data = []
    languages = Language.query.all()
    for language in languages:
        data.append({'value': language.num, 'name': language.name})
    data = sorted(data, key=lambda x: x['value'], reverse=True)[0:10]
    return jsonify({'data': data})


@app.route("/movie/country")
def country_static():
    data = []
    countrys = Country.query.all()
    for country in countrys:
        data.append({'value': country.num, 'name': country.en_name})
    return jsonify({'data': data})


@app.route("/movie/year")
def year_produce():
    year_num = db.session.query(Movie.year, db.func.count('*').label('year_group')).group_by(Movie.year).all()
    return jsonify({'data': year_num})


@app.route("/movie/length")
def movie_length():
    length = db.session.query(Movie.length, db.func.count('*').label('length_group')).group_by(Movie.length).all()
    return jsonify({'data': length})


@app.route("/movie/rateline")
def rateline():
    rate_static = db.session.query(Movie.score, db.func.count('*').label('rate_group')).group_by(Movie.score).all()
    return jsonify({'data': rate_static})


@app.route("/movie/year_relation")
def relationy():
    year = db.session.query(Movie.year, Movie.score).all()
    return jsonify({'data': year})

@app.route("/movie/length_relation")
def relationl():
    length = db.session.query(Movie.length, Movie.score).all()
    return jsonify({'data': length})


# @app.route("/movie/description")
# def description():
#     movie_list = []
#     des = Movie.query.order_by(db.desc(Movie.score)).limit(10).all()
#     for item in des:
#         movie = {}
#         tags = item.tags.all()
#         languages = item.languages.all()
#         countries = item.countries.all()
#         movie['tag'] = reduce(lambda x, y: x+"/"+y, map(lambda x : x.name, tags))
#         movie['languages'] = reduce(lambda x, y: x+" "+y, map(lambda x: x.name, languages))
#         movie['countries'] = reduce(lambda x, y: x+" "+y, map(lambda x: x.name, countries))
#         movie['name'] = item.name
#         movie['director'] = item.director
#         movie['scriptwriter'] = item.screenwriter
#         movie['length'] = item.length
#         movie['othername'] = item.othername
#         movie['score'] = item.score
#         movie['release_time'] = item.release_time
#         movie['mainactors'] = item.mainactors
#         movie['cover'] = item.cover
#         movie['summary'] = item.summary
#         movie['imdblink'] = item.imdb_url
#         movie_list.append(movie)
#
#     return jsonify({'data': movie_list})
#

@app.route("/movie/keyword", methods=['POST'])
def keyword():
    movie_list = []
    data = request.form
    keyword = data['keyword']
    movie_result = Movie.query.filter(Movie.name.like('%'+keyword+'%')).limit(10).all()
    for item in movie_result:
        movie = {}
        movie['tag'] = item.tags
        movie['languages'] = item.languages
        movie['countries'] = item.countrys
        movie['name'] = item.name
        movie['director'] = item.director
        movie['scriptwriter'] = item.screenwriter
        movie['length'] = item.length
        movie['othername'] = item.othername
        movie['score'] = item.score
        movie['release_time'] = item.release_time
        movie['mainactors'] = item.mainactors
        movie['cover'] = item.cover
        movie['summary'] = item.summary
        movie['imdblink'] = item.imdb_url
        movie['shortcomnum'] = item.shortcomnum
        movie['commentnum'] = item.commentnum
        movie_list.append(movie)
    
    return jsonify({'data': movie_list})

# @app.route("/movie/keyword", methods=['POST'])
# def keyword():
#     movie_list = []
#     data = request.form
#     keyword = data['keyword']
#     res = Movie.query.filter(Movie.name.like('%%%'+keyword+'%').all()
#     for item in res:
#         print('hello')
#     return jsonify({"movies": movie_list})