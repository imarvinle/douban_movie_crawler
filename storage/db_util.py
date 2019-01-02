# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
-------------------------------------------------
   Description :  数据库插入操作
   Author :       lichunlin
   date：          2018/12/31
-------------------------------------------------
'''

from storage import Session
from storage.map_config import nameMap, language_map
from storage.model import Movie, Tag, Country, Language

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
        tags = ""
        for tag_str in movie.tags:
            tags = tags + "/" + tag_str
            # tag = self.session.query(Tag).filter_by(name=tag_str).first()
            # if tag:
            #     tag.num = tag.num + 1
            #     tag_list.append(tag)
            # else:
            #     tag_list.append(Tag(tag_str, 1))
        tags = tags.strip("/")

        country_list = []
        countrys = ""
        for country_str in movie.countries:
            countrys = countrys + "/" +country_str
            en_country_str = nameMap.get(country_str, "China")
            # country = self.session.query(Country).filter_by(en_name=country_str).first()
            # if country:
            #     country.num = country.num + 1
            #     country_list.append(country)
            # else:
            #country_list.append(Country(country_str, en_country_str, 1))
        countrys = countrys.strip("/")

        language_list = []
        languages = ""
        for language_str in movie.languages:
            language_str = language_map.get(language_str, language_str)
            languages = languages + "/" + language_str
            # language = self.session.query(Language).filter_by(name=language_str).first()
            # if language:
            #     language.num = language.num + 1
            #     language_list.append(language)
            #else:
            #language_list.append(Language(language_str, 1))
        languages = languages.strip("/")
        new_movie = None
        try:
            new_movie = Movie(movie.title, movie.movie_id, movie.cover, movie.summary, movie.director, movie.screenwriter, movie.release_time,
                              movie.length, movie.imdb_url, movie.othername, movie.score, movie.mainactors,movie.evaluation_nums,
                              movie.shortcomnum, movie.commentnum, movie.year, languages, countrys, tags,language_list, tag_list, country_list)
            self.session.add(new_movie)
            self.session.commit()
            print("[DB-OK] 电影 <%s> 已插入数据库\n" % (movie.title))
        except Exception as e:
            self.session.rollback()
            print("电影插入出错[%s]" % (str(new_movie)))
            print("DB Error  <%s>" % str(e))
        finally:
            self.session.close()


    def insert_short(self, short_list):
        try:
            self.session.add_all(short_list)
            self.session.commit()
            print("[短评-OK] %d 条短评已插入数据库\n" % len(short_list))

        except Exception as e:
            self.session.rollback()
            self.session.close()
            print("短评插入出错[%d 条短评]" % (len(short_list)))
            print("DB Error  <%s>" % str(e))
        finally:
            self.session.close()

    def insert_comment(self, comment_list):
        try:

            self.session.add_all(comment_list)
            print("[影评-OK] %d 条影评已插入数据库\n" % len(comment_list))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            print("影评插入数据出错[%d条影评]" % len(comment_list))
            print("DB Error  <%s>" % str(e))
        finally:
            self.session.close()

    def insert_shortcrawed(self, shortcrawed):
        try:
            self.session.add(shortcrawed)
            self.session.commit()
            print("电影[%s] 短评已全部插入数据库\n" % shortcrawed.movie_name)
        except Exception as e:
            self.session.rollback()
            self.session.close()
            print("短评标记插入出错[%s]" % (str(shortcrawed)))
            print("DB Error  <%s>" % str(e))
        finally:
            self.session.close()

    def insert_commentcrawed(self, commentcrawed):
        try:
            self.session.add(commentcrawed)
            self.session.commit()
            print("电影[%s] 影评已全部插入数据库\n" % commentcrawed.movie_name)
        except Exception as e:
            self.session.rollback()
            self.session.close()
            print("影评标记插入出错 [%s]" % (str(commentcrawed)))
            print("DB Error  <%s>" % str(e))
        finally:
            self.session.close()



