#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import random

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

from app.models.model import Movie, Tag



@app.route('/')
def hello_world():
    return render_template('test.html')

@app.route('/index')
def test():
    return render_template('index.html')

@app.route('/rate')
def rate():
    return render_template('rate.html')

@app.route('/search')
def search():
    movie_list = []
    des = Movie.query.order_by(db.desc(Movie.shortcomnum)).limit(12).all()
    for item in des:
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
    return render_template('search.html', movies=movie_list)



# 导入router  (新定义的router文件必须在这里导入才能被注册)

from app.routes import movie
