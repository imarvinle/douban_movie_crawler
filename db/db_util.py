# -*-coding: utf-8 -*-
from db import Session
from db.model import Movie, Tag, Country, Comment, Language, ENCountry
from db.map_config import nameMap

language_map = {"汉语普通话": "汉语", "美国": "英语", "加拿大": "英语","四川话": "汉语", "山西话": "汉语", "俄罗斯":"俄语",
                "印度": "印度语","中国大陆": "汉语", "德国": "德语", "香港":"粤语", "意大利":"意大利语", "英国":"英语", "日本":"日语",
                "西安话" : "汉语", "台湾" : "汉语", "南京话": "汉语", "上海话": "汉语", "唐山话": "汉语", "韩国" : "汉语"}

def db_operate(type = None, value = None):
        session = Session()
        db_helper = DB_Helper(session)
        if type == "movie":
            db_helper.insert_movie(value)
        elif type == "short":
            db_helper.insert_short(value)
        elif type == "comment":
            db_helper.insert_comment(value)
        elif type == "shortid":
            db_helper.insert_shortcrawed(value)
        elif type == "commentid":
            db_helper.insert_commentcrawed(value)
        else:
            print("[Bad] 无法识别这个数据插入请求 <%s>" % str(type))

class DB_Helper():

    def __init__(self, session):
        self.session = session

    def insert_movie(self, movie):
        tag_list = []
        for tag_str in movie.tags:
            tag = self.session.query(Tag).filter_by(name=tag_str).first()
            if tag:
                tag_list.append(tag)
            else:
                tag_list.append(Tag(tag_str))
        country_list = []
        for country_str in movie.countries:
            country = self.session.query(Country).filter_by(name=country_str).first()
            if country:
                country_list.append(country)
            else:
                country_list.append(Country(country_str))

        en_country_list = []
        for en_country_str in movie.countries:
            en_country_str = nameMap.get(en_country_str, en_country_str)
            en_country = self.session.query(ENCountry).filter_by(name=en_country_str).first()
            if en_country:
                en_country_list.append(en_country)
            else:
                en_country_list.append(ENCountry(en_country_str))

        language_list = []
        for language_str in movie.languages:
            language_str = language_map.get(language_str, language_str)
            language = self.session.query(Language).filter_by(name=language_str).first()
            if language:
                language_list.append(language)
            else:
                language_list.append(Language(language_str))
        new_movie = None



        try:
            new_movie = Movie(movie.title, movie.movie_id, movie.cover, movie.summary, movie.director, movie.screenwriter, movie.release_time,
                              movie.length, movie.imdb_url, movie.othername, movie.score, movie.mainactors,
                              movie.evaluation_nums, movie.shortcomnum, movie.commentnum, movie.year,language_list, tag_list, country_list, en_country_list)
            self.session.add(new_movie)
            self.session.commit()
            print("[DB-OK] 电影 <%s> 已插入数据库\n" % (movie.title))
        except Exception as e:
            self.session.rollback()
            self.session.close()
            print("插入数据出错[%s]" % (str(new_movie)))
            print("DB Error  <%s>" % str(e))


    def insert_short(self, short_list):
        try:
            self.session.add_all(short_list)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            print("插入数据出错[%d 条短评]" % (len(short_list)))
            print("DB Error  <%s>" % str(e))

    def insert_comment(self, comment):
        new_comment = None
        try:
            new_comment = Comment(comment['movie_name'], comment['nickname'], comment['time'], comment['content'], comment['usednum'],
                              comment['unusednum'], comment['responsenum'])
            self.session.add(new_comment)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            print("插入数据出错[%s]" % (str(new_comment)))
            print("DB Error  <%s>" % str(e))

    def insert_shortcrawed(self, shortcrawed):
        try:
            self.session.add(shortcrawed)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            print("插入数据出错[%s]" % (str(shortcrawed)))
            print("DB Error  <%s>" % str(e))

    def insert_commentcrawed(self, commentcrawed):
        try:
            self.session.add(commentcrawed)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            print("插入数据出错[%s]" % (str(commentcrawed)))
            print("DB Error  <%s>" % str(e))




