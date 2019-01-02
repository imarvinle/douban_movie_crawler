#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from app import db, app
from app.models.model import Tag
from app.models.model import Movie
from app.models.model import Language, Country, ShortComment, Comment
from flask import jsonify, request, render_template
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

@app.route("/movie/heat")
def getheat():
    movie_list = []
    com_list = []
    have_name = set()
    movies = Movie.query.order_by(db.desc(Movie.shortcomnum)).limit(40).all()
    for movie in movies:
        name = movie.name
        if name not in have_name:
            shortcomnum = movie.shortcomnum
            movie_list.append(name)
            com_list.append(shortcomnum)
            have_name.add(name)
            if len(com_list) >=8:
                break
    return jsonify({'movies': movie_list, 'comments': com_list})

@app.route("/movie/shortcom/<name>")
def passing(name=''):
    comments_list = []
    name = name
    hava_nickname = set()
    comments = ShortComment.query.filter(ShortComment.movie_name == name).order_by(db.desc(ShortComment.likenum)).limit(60).all()
    if len(comments) < 30:
        new_comments = ShortComment.query.limit(60-len(comments)).all()
        comments.extend(new_comments)
    for item in comments:
        if item.nickname not in hava_nickname:
            comment = {}
            comment['name'] = item.movie_name
            comment['nickname'] = item.nickname
            comment['time'] = item.time
            comment['content'] = item.content
            comment['likenum'] = item.likenum
            comment['avatar'] = item.avatar
            comments_list.append(comment)
            hava_nickname.add(item.nickname)
            if len(comments_list) >= 20:
                break
    return render_template('shortcom.html', comments=comments_list)

@app.route("/movie/comment/<name>")
def comment(name=''):
    comments_list = []
    have_nickname = set()
    name = name
    comments = Comment.query.filter(Comment.movie_name == name).order_by(db.desc(Comment.usednum)).limit(60).all()
    if len(comments) < 30:
        new_comments = Comment.query.limit(60 - len(comments)).all()
        comments.extend(new_comments)
    for item in comments:
        if item.nickname not in have_nickname:
            comment = {}
            comment['name'] = item.movie_name
            comment['id'] = item.id
            comment['nickname'] = item.nickname
            comment['usefulnum'] = item.usednum
            comment['uselessnum'] = item.unusednum
            comment['responsenum'] = item.responsenum
            comment['time'] = item.time
            comment['avatar'] = item.avatar
            comment['content'] = item.content
            comments_list.append(comment)
            have_nickname.add(item.nickname)
            if len(comments_list) >= 20:
                break
    return render_template('comment.html', comments=comments_list)

@app.route("/movie/keyword", methods=['POST'])
def keyword():
    movie_list = []
    have_name = set()
    data = request.form
    keyword = data['keyword']
    movie_result = Movie.query.filter(Movie.name.like('%'+keyword+'%')).all()
    for item in movie_result:
        if item.name not in have_name:
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
            have_name.add(item.name)
    
    return jsonify({'data': movie_list})
