from sqlalchemy import Column, String, Text, Integer, Table, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


tags = Table('tags',Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id', ondelete='CASCADE')),
    Column('movie_name', String(60), ForeignKey('movie.name', ondelete='CASCADE'))
)

en_countrys = Table('en_countrys',Base.metadata,
    Column('en_country_id', Integer, ForeignKey('en_country.id', ondelete='CASCADE')),
    Column('movie_name', String(60), ForeignKey('movie.name', ondelete='CASCADE'))
)


countrys = Table('countrys',Base.metadata,
    Column('country_id', Integer, ForeignKey('country.id', ondelete='CASCADE')),
    Column('movie_name', String(60), ForeignKey('movie.name', ondelete='CASCADE'))
)

languages = Table('languages',Base.metadata,
    Column('language_id', Integer, ForeignKey('language.id', ondelete='CASCADE')),
    Column('movie_name', String(60), ForeignKey('movie.name', ondelete='CASCADE'))
)

class Movie(Base):
    __tablename__ = "movie"

    name = Column(String(60), primary_key=True)
    id = Column(Integer, nullable=True)
    cover = Column(String(200), nullable=True)
    summary = Column(Text, nullable=True)
    director = Column(String(50), nullable=True)
    screenwriter = Column(String(100), nullable=True)
    mainactors = Column(Text, nullable=True)
    release_time = Column(String(100), nullable=True)
    length = Column(Integer, default=0)
    imdb_url = Column(String(200),nullable=True)
    othername = Column(String(260), nullable=True)
    score = Column(Float, default=5.0)
    evaluation_nums = Column(Integer, default=0)
    shortcomnum = Column(Integer, default=0)
    year = Column(Integer, default=2018)
    commentnum = Column(Integer, default=0)

    tags = relationship("Tag", secondary=tags, backref=backref("movie", lazy="joined"), lazy="dynamic")
    countries = relationship("Country", secondary=countrys, backref=backref("movie", lazy="joined"), lazy="dynamic")
    en_countries = relationship("ENCountry", secondary=en_countrys, backref=backref("movie", lazy="joined"), lazy="dynamic")

    languages = relationship("Language", secondary=languages, backref=backref("movie", lazy="joined"), lazy="dynamic")

    def __init__(self, name, movie_id, cover, summary, director, screenwriter , release_time, length, imdb_url,
                 othername, score, mainactors, evaluation_nums, shortcomnum, commentnum, year, languages = None, tags=None, country=None, encountry=None):
        self.name = name
        self.id = movie_id
        self.cover = cover
        self.summary = summary
        self.director = director
        self.screenwriter = screenwriter
        self.languages = languages
        self.release_time = release_time
        self.length = length
        self.imdb_url = imdb_url
        self.othername = othername
        self.score = score
        self.evaluation_nums = evaluation_nums
        self.mainactors  = mainactors
        self.tags = tags
        self.shortcomnum = shortcomnum
        self.commentnum = commentnum
        self.year = year
        self.countries = country
        self.en_countries = encountry

    def __repr__(self):
        return '<Movie %s  id=%d  短评: %d 影评: %d>' % (self.name, self.id, self.shortcomnum, self.commentnum)


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %s>' % self.name

class Language(Base):
    __tablename__ = 'language'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Language %s>' % self.name


class Country(Base):
    __tablename__ = "country"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Country %s>' % self.name

class ENCountry(Base):
    __tablename__ = "en_country"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<ENCountry %s>' % self.name


class ShortComment(Base):
    __tablename__ = "shortcom"


    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String(60), ForeignKey('movie.name', ondelete='CASCADE'))
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
        return '<ShortCom %s %s %s  %d>' % (self.movie_name, self.nickname, self.time, self.likenum)


class Comment(Base):
    __tablename__ = "comment"

    # 影评者昵称、影评时间、影评内容、认为有用人数、认为无用人数、转发人数、回应人数等信

    #  主键
    id = Column(Integer, primary_key=True, autoincrement=True)
    movie_name = Column(String(60), ForeignKey('movie.name', ondelete='CASCADE'))
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
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String(60), nullable=True)

    def __init__(self, movie_id, movie_name):
        self.movie_id = movie_id
        self.movie_name = movie_name

    def __repr__(self):
        return '<CommentCrawed %s  ID %d>' % (self.movie_name, self.movie_id)


class ShortCommentCrawed(Base):
    __tablename__ = "shortcrawed"
    movie_id = Column(Integer, primary_key=True)
    movie_name = Column(String(60), nullable=True)

    def __init__(self, movie_id, movie_name):
        self.movie_id = movie_id
        self.movie_name = movie_name

    def __repr__(self):
        return '<ShortCommentCrawed %s  ID %d>' % (self.movie_name, self.movie_id)
