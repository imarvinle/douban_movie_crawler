from app import db


tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id', ondelete='CASCADE')),
    db.Column('movie_id', db.String(60), db.ForeignKey('movie.id', ondelete='CASCADE'))
)

countrys = db.Table('countrys',
         db.Column('country_id', db.Integer, db.ForeignKey('country.id', ondelete='CASCADE')),
         db.Column('movie_id', db.String(60), db.ForeignKey('movie.id', ondelete='CASCADE'))
)

languages = db.Table('languages',
    db.Column('language_id', db.Integer, db.ForeignKey('language.id', ondelete='CASCADE')),
    db.Column('movie_id', db.String(60), db.ForeignKey('movie.id', ondelete='CASCADE'))
)





class Movie(db.Model):
    __tablename__ = "movie"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), index=True)
    movie_id = db.Column(db.Integer, nullable=True)
    cover = db.Column(db.String(300), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    director = db.Column(db.String(100), nullable=True)
    screenwriter = db.Column(db.Text, nullable=True)
    mainactors = db.Column(db.Text, nullable=True)
    release_time = db.Column(db.String(200), nullable=True)
    length = db.Column(db.Integer, default=0)
    imdb_url = db.Column(db.String(200),nullable=True)
    othername = db.Column(db.Text, nullable=True)
    score = db.Column(db.Float, default=5.0,index=True)
    evaluation_nums = db.Column(db.Integer, default=0)
    shortcomnum = db.Column(db.Integer, default=0)
    year = db.Column(db.Integer, default=2018)
    commentnum = db.Column(db.Integer, default=0)

    tag_list = db.relationship("Tag", secondary=tags, backref=db.backref("movie", lazy="select"), lazy="select")
    country_list = db.relationship("Country", secondary=countrys, backref=db.backref("movie", lazy="select"), lazy="select")
    language_list = db.relationship("Language", secondary=languages, backref=db.backref("movie", lazy="select"), lazy="select")

    tags = db.Column(db.Text, nullable=True)
    countrys = db.Column(db.Text, nullable=True)

    languages = db.Column(db.Text, nullable=True)
    def __init__(self, name, id, cover, summary, director, screenwriter , release_time, length, imdb_url,
                 othername, score, mainactors, evaluation_nums, shortcomnum, commentnum, year, languages, countrys, tags,
                 language_list=None,tag_list=None, country_list=None):
        self.name = name
        self.id = id
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

        self.languages =languages
        self.countrys = countrys
        self.tags = tags

        self.language_list = language_list
        self.tag_list = tag_list
        self.country_list = country_list

    def __repr__(self):
        return '<Movie %s 短评: %d 影评: %d>' % (self.name, self.shortcomnum, self.commentnum)


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), index=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %s>' % self.name


class Country(db.Model):
    __tablename__ = "country"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), index=True)
    en_name = db.Column(db.String(60))

    def __init__(self, name, en_name):
        self.name = name
        self.en_name = en_name
    def __repr__(self):
        return '<Country name=%s  en_name=%s>' % (self.name, self.en_name)


class Language(db.Model):
    __tablename__ = 'language'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), index=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Language %s>' % self.name



class ShortComment(db.Model):
    __tablename__ = "shortcom"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(100), index=True)
    nickname = db.Column(db.String(60), nullable=True)
    time = db.Column(db.String(60), nullable=True)
    content = db.Column(db.Text, nullable=True)
    likenum = db.Column(db.Integer, default=0)

    def __init__(self, movie_name, nickname, _time, content, likenum):
        self.movie_name = movie_name
        self.nickname = nickname
        self.time = _time
        self.content = content
        self.likenum = likenum

    def __repr__(self):
        return '<ShortCom %s %s %s  %d>' % (self.movie_name, self.nickname, self.time, self.likenum)


class Comment(db.Model):
    __tablename__ = "comment"

    # 影评者昵称、影评时间、影评内容、认为有用人数、认为无用人数、转发人数、回应人数等信

    #  主键
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(100), index=True)
    nickname = db.Column(db.String(60), nullable=True)
    time = db.Column(db.String(60), nullable=True)
    content = db.Column(db.Text, nullable=True)
    usednum = db.Column(db.Integer, default=0)
    unusednum = db.Column(db.Integer, default=0)
    responsenum = db.Column(db.Integer, default=0)


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

