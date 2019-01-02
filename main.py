# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
-------------------------------------------------
   Description :  启动文件
   Author :       lichunlin
   date：          2018/12/31
-------------------------------------------------
'''

from queue import Queue

from crawler.movie import *
from thread.thread_pool import *
from storage import Session
from storage.model import Movie, ShortCommentCrawed, CommentCrawed
from crawler.comment import craw_comment_list
from crawler.shortcomment import craw_shortcomment
from crawler import MyOpener
from config import TagThreadSize, MovieThreadSize, ShortCommentSize, CommentSize, DataBaseInsertSize

ISOTIMEFORMAT='%Y-%m-%d %X'

all_movie_id = set()
all_movie_name = set()
comment_id = set()
short_id = set()
movie_map = dict()

tag_list = [
            "剧情", "喜剧", "动作", "爱情", "科幻", "动画", "悬疑", "惊悚", "恐怖", "犯罪",
            "同性", "音乐", "歌舞", "传记", "历史", "战争", "西部", "奇幻", "冒险", "灾难",
            "武侠", "情色", "儿童", "古装", "运动", "同性", "纪录片", "戏曲"
            ]


tags = set(tag_list)

def query():
    global all_movie_id
    global all_movie_name
    global comment_id
    global short_id
    global movie_map

    session = Session()
    movies = session.query(Movie.movie_id, Movie.name, Movie.commentnum, Movie.shortcomnum)
    all_movie_id = set(map(lambda x: x[0], movies))
    for item in movies:
        movie_map[item[0]] = {"name": item[1], "comnum": item[2], "shortnum": item[3]}

    all_movie_name = set(map(lambda x: x[1].strip(), movies))

    shorts = session.query(ShortCommentCrawed.movie_id)
    short_id = set(map(lambda x: x[0], shorts))

    comments = session.query(CommentCrawed.movie_id)
    comment_id = set(map(lambda x: x[0], comments))




def main():
    # 查询
    global comment_id
    global short_id
    global all_movie_id
    global tags

    query()

    # 求差集合
    print("********** START **********")
    print(time.strftime(ISOTIMEFORMAT, time.localtime()))
    print("**********统计信息 *********")
    print("已经抓取 %d 部电影" % len(all_movie_name))
    print("已经抓取短评的电影有 %d 部" % len(short_id))
    print("已经抓取评论的电影有 %d 部" % len(comment_id))

    comment_id = all_movie_id.difference(comment_id)
    short_id = all_movie_id.difference(short_id)
    print("还未抓取短评的电影有 %d 部" % len(short_id))
    print("还未抓取影评的电影有 %d 部" % len(comment_id))
    print("将把未抓取短评、影评的电影投入队列")
    userin = input("输入y开始爬取: ")
    if userin != "y" and userin != "Y":
        print("\nBye")
        return

    r = MyOpener("tag").open("http://movie.douban.com/j/search_tags?type=movie&source=")
    if not r["result"]:
        print("tag获取失败")
        return


    new_tags = json.loads(r["data"].text)['tags']
    tags.update(new_tags)

    print("共有: %d 类电影" % len(tags))
    movie_tag_queue = Queue(2000)
    movie_queue = Queue(40000)
    shortqueue = Queue(40000)
    commentqueue = Queue(40000)
    db_queue = Queue(100000)

    #加入影评队列
    for id in comment_id:
        movie = movie_map[id]
        commentqueue.put((craw_comment_list, [id, movie['name'], movie['comnum'], db_queue], {}))

    # 加入短评队列
    for id in short_id:
        movie = movie_map[id]
        shortqueue.put((craw_shortcomment, [id, movie['name'], movie['shortnum'], db_queue], {}))
    tags_list = []
    for tag in tags:
        tags_list.append(tag)

    for tag in tags_list:
        movie_tag_queue.put((craw_movie_id, [tag, movie_queue, shortqueue, commentqueue, db_queue], {}))

    pool = MyThreadPool(movie_tag_queue, movie_queue, shortqueue, commentqueue, db_queue, TagThreadSize,
                        MovieThreadSize, ShortCommentSize,CommentSize,DataBaseInsertSize)
    pool.joinAll()
    print("********** END **********")
    print(time.strftime(ISOTIMEFORMAT, time.localtime()))
if __name__ == "__main__":
    main()
