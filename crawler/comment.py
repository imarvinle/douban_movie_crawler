# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
-------------------------------------------------
   Description :  爬取电影评论
   Author :       lichunlin
   date：          2018/12/30
-------------------------------------------------
'''

import re
import time
import traceback
from bs4 import BeautifulSoup
from storage.db_util import db_operate
from crawler import MyOpener
from storage.model import CommentCrawed, Comment


def craw_comment_list(movie_id, movie_name, commentnum, db_queue):
    errornum = 0
    comment_crawed = CommentCrawed(movie_id, movie_name)
    opener = MyOpener("[%s]影评" % movie_name)
    comment_list = []
    pagenum = commentnum // 20
    if pagenum % 20 > 0:
         pagenum = pagenum + 1
    for i in range(pagenum):
        print("********** 正在爬取电影 <%s> 的第 %d 页的影评**********\n" % (movie_name, i+1))
        url = "https://movie.douban.com/subject/%d/reviews?sort=hotest&start=%d" % (movie_id, 20 * i)

        if i > 20:
            break
        res = opener.open(url)

        if not res["result"]:
            print("电影<%s> 第 %d 页影评爬取失败\n" % (movie_name, i+1))
            errornum = errornum + 1
            if errornum > 100:
                print(" 停止爬取电影 <%s> 影评共爬取 %d 页\n" % (movie_name, i))
                break
            else:
                continue

        html = res["data"].text
        try:
            soup = BeautifulSoup(html, "html.parser")
            review_list = soup.select("div.review-list  ")[0]
            review_list = review_list.select("> div")
            for review_item in review_list:
                try:
                    avatar = review_item.select("img")
                    if len(avatar) > 0:
                        avatar = avatar[0]["src"].strip()
                    else:
                        avatar = "https://img1.doubanio.com/icon/u64304532-9.jpg"
                    nickname = review_item.select("a.name")[0].get_text().split()[0]
                    _time = review_item.select("span.main-meta")[0].get_text().split()[0]
                    contents = review_item.select("div.short-content")[0].get_text().split()
                    content = ""
                    for item in contents:
                        content = content + " " + item.strip()
                    actions = review_item.select("div.action > a")
                    usednum = 0
                    unusednum = 0
                    used = actions[0].select("span")[0].get_text().split()
                    if used:
                        usednum = int(used[0])
                    unused = actions[1].select("span")[0].get_text().split()

                    if unused:
                        unusednum = int(unused[0])
                    responsestr = actions[2].get_text().split()[0]
                    responsenum = int(re.compile(r'[0-9]\d*').findall(responsestr)[0])

                    comment = Comment(avatar, movie_name, nickname, _time, content, usednum, unusednum, responsenum)

                    comment_list.append(comment)
                except Exception as e:
                    print("解析电影<%s> 第 %d 页影评出错\n" %(movie_name, i+1))
                    continue

            if i % 4 == 0:
                db_queue.put((db_operate, [], {"value": comment_list, "type": "comment"}))
                comment_list = []
        except Exception as e:
            info = traceback.format_exc()
            print(info)
            errornum = errornum + 1
            if errornum > 100:
                print(" 停止爬取电影 <%s> 影评共爬取 %d 页\n" % (movie_name, i))
                break
            else:
                continue
        time.sleep(2)
    if len(comment_list) > 0:
        db_queue.put((db_operate, [], {"value": comment_list, "type": "comment"}))
    db_queue.put((db_operate, [], {"value": comment_crawed, "type": "commentid"}))







