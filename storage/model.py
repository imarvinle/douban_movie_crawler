# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
-------------------------------------------------
   Description :  定义ORM模型
   Author :       lichunlin
   date：          2018/12/31
-------------------------------------------------
'''


from sqlalchemy import Column, String, Text, Integer, Table, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


tags = Table('tags',Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete='CASCADE')),
    Column('movie_id', Integer, ForeignKey('movie.id', ondelete='CASCADE'))
)

countrys = Table('countrys',Base.metadata,
    Column('country_id', Integer, ForeignKey('country.id', ondelete='CASCADE')),
    Column('movie_id', Integer, ForeignKey('movie.id', ondelete='CASCADE'))
)

languages = Table('languages',Base.metadata,
    Column('language_id', Integer, ForeignKey('language.id', ondelete='CASCADE')),
    Column('movie_id', Integer, ForeignKey('movie.id', ondelete='CASCADE'))
)

class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=True, index=True)
    movie_id = Column(Integer, nullable=True)
    cover = Column(String(300), nullable=True)
    summary = Column(Text, nullable=True)
    director = Column(String(100), nullable=True)
    screenwriter = Column(Text, nullable=True)
    mainactors = Column(Text, nullable=True)
    release_time = Column(String(200), nullable=True)
    length = Column(Integer, default=0)
    imdb_url = Column(String(200),nullable=True)
    othername = Column(Text, nullable=True)
    score = Column(Float, default=5.0, index=True)
    evaluation_nums = Column(Integer, default=0)
    shortcomnum = Column(Integer, default=0)
    year = Column(Integer, default=2018)
    commentnum = Column(Integer, default=0)
    tag_list = relationship("Tag", secondary=tags, backref=backref("movie", lazy="joined"), lazy="dynamic")
    country_list = relationship("Country", secondary=countrys, backref=backref("movie", lazy="joined"), lazy="dynamic")
    language_list = relationship("Language", secondary=languages, backref=backref("movie", lazy="joined"), lazy="dynamic")

    tags = Column(Text, nullable=True)
    countrys = Column(Text, nullable=True)
    languages = Column(Text, nullable=True)

    def __init__(self, name, movie_id, cover, summary, director, screenwriter , release_time, length, imdb_url,
                 othername, score, mainactors, evaluation_nums, shortcomnum, commentnum, year, languages, countrys, tags,
                 language_list = None, tag_list=None, country_list=None):
        self.name = name
        self.movie_id = movie_id
        self.cover = cover
        self.summary = summary
        self.director = director
        self.screenwriter = screenwriter
        self.release_time = release_time
        self.length = length
        self.imdb_url = imdb_url
        self.othername = othername
        self.score = score
        self.evaluation_nums = evaluation_nums
        self.mainactors  = mainactors
        self.shortcomnum = shortcomnum
        self.commentnum = commentnum
        self.year = year

        self.tags = tags
        self.languages = languages
        self.countrys = countrys
        self.tag_list = tag_list
        self.country_list = country_list
        self.language_list  = language_list


    def __repr__(self):
        return '<Movie %s  movie_id=%d  短评: %d 影评: %d>' % (self.name, self.movie_id, self.shortcomnum, self.commentnum)


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), index=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %s>' % self.name

class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), index=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Language %s>' % self.name


class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50), index=True)
    en_name = Column(String(60))

    def __init__(self, name, en_name):
        self.name = name
        self.en_name = en_name

    def __repr__(self):
        return '<Country name=%s  en_name=%s>' % (self.name, self.en_name)


class ShortComment(Base):
    __tablename__ = "shortcom"


    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String(60), index=True) #ForeignKey('movie.name', ondelete='CASCADE'))
    nickname = Column(String(60), nullable=True)
    time = Column(String(60), nullable=True)
    content = Column(Text, nullable=True)
    likenum = Column(Integer, default=0)

    def __init__(self, movie_name, nickname, _time, content, likenum):
        self.movie_name = movie_name
        self.nickname = nickname
        self.time = _time
        self.content = content
        self.likenum = likenum

    def __repr__(self):
        return '<ShortCom 电影:%s 评论者:%s 评论时间:%s>' % (self.movie_name, self.nickname, self.time)


class Comment(Base):
    __tablename__ = "comment"

    # 影评者昵称、影评时间、影评内容、认为有用人数、认为无用人数、转发人数、回应人数等信

    #  主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String(60), index=True)
    nickname = Column(String(60), nullable=True)
    time = Column(String(60), nullable=True)
    content = Column(Text, nullable=True)
    usednum = Column(Integer, default=0)
    unusednum = Column(Integer, default=0)
    responsenum = Column(Integer, default=0)


    def __init__(self, movie_name, nickname, _time, content, usednum, unusednum, responsenum):
        self.movie_name = movie_name
        self.nickname = nickname
        self.time = _time
        self.content = content
        self.usednum = usednum
        self.unusednum = unusednum
        self.responsenum = responsenum

    def __repr__(self):
        return '<Comment 电影:%s  评论者:%s  评论时间:%s>' % (self.movie_name, self.nickname, self.time)


class CommentCrawed(Base):
    __tablename__ = "commentcrawed"
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, nullable=True)
    movie_name = Column(String(60), nullable=True)

    def __init__(self, movie_id, movie_name):
        self.movie_id = movie_id
        self.movie_name = movie_name

    def __repr__(self):
        return '<CommentCrawed %s  ID %d>' % (self.movie_name, self.movie_id)


class ShortCommentCrawed(Base):
    __tablename__ = "shortcrawed"
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_id = Column(Integer, nullable=True)
    movie_name = Column(String(60), nullable=True)

    def __init__(self, movie_id, movie_name):
        self.movie_id = movie_id
        self.movie_name = movie_name

    def __repr__(self):
        return '<ShortCommentCrawed %s  ID %d>' % (self.movie_name, self.movie_id)
