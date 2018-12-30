# -*- coding: utf-8 -*-

import re
import time
import traceback

# 编码信息，生成请求，打开页面获取内容
from bs4 import BeautifulSoup

from db.db_util import db_operate
from crawers import MyOpener


# cookies处理


def craw_comment_list(movie_id, movie_name, commentnum, db_queue):
    errornum = 0
    opener = MyOpener("[%s]影评")
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
            if errornum > 3:
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
                nickname = review_item.select("a.name")[0].get_text().split()[0]
                _time = review_item.select("span.main-meta")[0].get_text().split()[0]
                content = review_item.select("div.short-content")[0].get_text().split()[0]
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

                comment = {
                    "movie_name": movie_name,
                    "nickname": nickname,
                    "time": _time,
                    "content": content,
                    "usednum": usednum,
                    "unusednum" : unusednum,
                    "responsenum": responsenum
                }
                with open("pinglun.txt", "a") as file:
                    file.write(str(comment))
                    file.write("\n")

                db_queue.put((db_operate, [], {"value": comment, "type": "comment"}))
        except Exception as e:
            info = traceback.format_exc()
            print("[%s]评论爬取异常, 停止爬取" % str(e))
            break
        time.sleep(4)







