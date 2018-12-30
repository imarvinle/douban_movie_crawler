
# cookies和请求处理
import json
import threading
import time
from urllib import parse

from bs4 import BeautifulSoup

from crawers import MyOpener
from db.db_util import db_operate
from main import all_movie_id, all_movie_name
import random

lock = threading.Lock()

def craw_movie_detail(movie_id, cover, title, score, short_queue, comment_queue, db_queue):
    movie_crawer = Moview_Crawer(movie_id, db_queue, short_queue, comment_queue, cover, title, score)
    movie_crawer.get_movie_detail()

def craw_movie_id(tag, movie_queue, short_queue, comment_queue, db_queue):
    start = 0
    opener = MyOpener("[%s标签包含电影抓取]" % tag)
    scores = [4.5, 5.6, 7.8, 8.9, 9.6]

    while True:
        url = "http://movie.douban.com/j/search_subjects?type=movie&tag=" + tag + "&page_limit=20&page_start=" + str(start)
        url = parse.quote(url, safe='/:?=&')

        res = opener.open(url)

        if not res["result"]:
            print("标签 <%s> 爬取失败\n" % (tag))
            break

        movies = json.loads(res["data"].text)['subjects']

        if len(movies) == 0:
            break
        for item in movies:
            if item["rate"]:
                score = float(item['rate'])
            else:
                score = random.choice(scores)
            title = item['title'].strip()
            cover = item['cover']
            id = int(item["id"])
            if lock.acquire():
                try:
                    if title not in all_movie_name:
                        all_movie_name.add(title)
                        movie_queue.put((craw_movie_detail, [id, cover, title, score, short_queue, comment_queue, db_queue], {}))
                    else:
                        print("发现重复电影[%s]" % title)
                finally:
                    lock.release()
        start = start + 20
        time.sleep(6)

    print("<%s> 类电影共有 %d 部\n" % (tag, start+20))




class Moview_Crawer():

    def __init__(self, movie_id, db_queue = None, short_queue = None, comment_queue = None, cover=None, title=None, score=None):
        self.short_queue = short_queue
        self.comment_queue = comment_queue
        self.db_queue  = db_queue

        self.opener = MyOpener("电影[%s]详情抓取" % str(title))
        self.movie_id = movie_id
        self.cover = cover
        self.title = title
        self.score = score
        self.screenwriter = ""
        self.director = ""
        self.summary = ""
        self.mainactors = ""
        self.tags = []
        self.countries = []
        self.languages = []
        self.release_time = ""
        self.length = 0
        self.imdb_url = ""
        self.othername = ""
        self.evaluation_nums = 0
        self.shortcomnum = 0
        self.commentnum = 0
        self.year = 2018


    def get_movie_detail(self):
        url = "https://movie.douban.com/subject/%s/?from=gaia" % str(self.movie_id)

        res = self.opener.open(url)
        if not res["result"]:
            print("电影 <%s> 爬取失败\n" % self.title)
            return

        html = res["data"].text

        try:
            soup = BeautifulSoup(html, "html.parser")

            ## 主演 剧情简介 编剧 导演
            self.summary = soup.select('span[property="v:summary"]')[0].get_text().split()[0]
            self.director = soup.select('a[rel="v:directedBy"]')[0].get_text().split()[0]

            screenwriters = soup.select("div#info > span")[1].select("a")
            actors = soup.select("div#info > span")[2].select("a")

            for item in screenwriters:
                self.screenwriter = self.screenwriter + "/" + item.get_text().split()[0]
            self.screenwriter = self.screenwriter.strip('/')

            for item in actors:
                self.mainactors = self.mainactors + "/" + item.get_text().split()[0]
            self.mainactors = self.mainactors.strip('/')
            ## 类型
            types = soup.select("div#info > span[property='v:genre']")
            for item in types:
                if item != "":
                    self.tags.append(item.get_text().split()[0])
            ## 国家
            countries = soup.select("div#info > span.pl")[1].next_sibling.string.split('/')
            for item in countries:
                if item.strip() != "":
                    self.countries.append(item.strip())
            ## 语言
            language = soup.select("div#info > span.pl")[2].next_sibling.string.strip()
            for item in language.split("/"):
                if item.strip() != "":
                    self.languages.append(item.strip())


            ## 上映日期
            release_times = soup.select("div#info > span[property='v:initialReleaseDate']")
            for item in release_times:
                self.release_time = self.release_time + "/" + item.get_text().split()[0]
            self.release_time = self.release_time.strip('/')
            ## 片长
            length = soup.select("div#info > span[property='v:runtime']")[0]["content"].strip()
            self.length = int(length)
            ## imdb链接
            self.imdb_url = soup.select("div#info > a[rel='nofollow']")[0]["href"].strip()
            ## 又名
            othernames = soup.select("div#info > span.pl")[5].next_sibling.string.split('/')
            for item in othernames:
                self.othername = self.othername + '/' + item.strip()
            self.othername = self.othername.strip('/')
            ## 评分人数
            self.evaluation_nums = int(soup.select("span[property='v:votes']")[0].get_text().split()[0])

            ## 短评人数
            shortcomnum = soup.select("div#comments-section > div.mod-hd")[0].select("span.pl")[0].select("a")[0].get_text().strip()
            self.shortcomnum = int(shortcomnum.split(" ")[1])
            ## 评论人数
            self.commentnum = int(soup.select("a[href='reviews']")[0].get_text().strip().split(" ")[1])

            ## 年份
            self.year = int(soup.select("span.year")[0].get_text().strip("()").strip())

            self.db_queue.put((db_operate, [], {"value": self, "type": "movie"}))
            print("[Movie-OK] 电影 <%s> 爬取成功" % self.title)
            # self.short_queue.put((craw_shortcomment, [self.title, self.movie_id, self.shortcomnum, self.db_queue], {}))
            # self.comment_queue.put((craw_comment_list, [self.movie_id, self.title, self.commentnum, self.db_queue], {}))
        except Exception as e:
            print("MovieDetail Exception <%s>" % (str(e)))
            print("[Bad] 电影 <%s> 爬取失败\n" % self.title)
        time.sleep(4)


