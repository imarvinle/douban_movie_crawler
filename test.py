
from crawers import headers
import urllib
import requests
import json
from urllib import  *
import time
from http import cookiejar
from crawers.shortcomment import ShortComment_Crawer
from crawers.comment import craw_comment_list
from bs4 import BeautifulSoup
import random
import string
from urllib import parse
from crawers import MyOpener as Opner

def craw_movie_id(tag, movie_queue, short_queue, comment_queue, db_queue):
    start = 0
    opener = Opner("[%s标签包含电影抓取]" % tag)

    while True:
        #"https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags="
        "https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=%E7%94%B5%E5%BD%B1&start=20&genres=%E5%96%9C%E5%89%A7"
        url = "http://movie.douban.com/j/search_subjects?type=movie&tag=" + tag + "&page_limit=20&page_start=" + str(start)
        url = parse.quote(url, safe='/:?=&')

        res = opener.open(url)
        print(res["data"].text)
        if not res["result"]:
            print("标签 <%s> 爬取失败\n" % tag)
            break

        movies = json.loads(res["data"].text)['subjects']

        if len(movies) == 0:
            break
        for item in movies:

            #score = float(item['rate'])
            title = item['title']
            cover = item['cover']
            id = int(item["id"])
            print(title)
        start = start + 20
        time.sleep(1)

    print("<%s> 类电影共有 %d 部\n" % (tag, start+20))



class ProxyProvider():

    def __init__(self):
        self.ipcache = set()

    def get_addr(self):
        if len(self.ipcache) == 0:
            req = requests.get("https://proxy.horocn.com/api/proxies?order_id=NWRK1621240083969632&num=10&format=json&line_separator=win").text
            req_json = json.loads(req)
            print(req_json)
            for item in req_json:
                ip = item['host'] + ":" + str(item['port'])
                print(ip)
                self.ipcache.add(ip)
            print("重新拉取20条代理")
        return self.ipcache.pop()


    def delete_addr(self, ip):
        # req = requests.get(("http://39.108.123.85:8000/delete?ip=%s" % ip)).content
        # print(req)
        pass



class MyOpener():

    def __init__(self, request_session):
        self.session = request_session
        self.proxy_provider = ProxyProvider()
        self.proxyaddr = self.proxy_provider.get_addr()
        self.proxy = {
            'http': 'http://' + self.proxyaddr,
            'https': 'https://' + self.proxyaddr,
        }


    def open(self, req):
        print("当前使用的代理: %s" % self.proxyaddr)
        retrynum = 0
        response = None
        while True:
            try:
                response = self.session.get(req,  timeout=5)        #proxies = self.proxy,

            except requests.exceptions.RequestException as e:
                retrynum = retrynum + 1
                print("出错啦 <%s>" % str(e))
                self.update_proxy()
                if retrynum > 5:
                    response = None
                    break

        if response ==  None:
            return False
        else:
            if response.status_code != 200:
                print("返回吗不是200")
                self.update_proxy()
            return response


    def update_proxy(self):
        self.proxy_provider.delete_addr(self.proxyaddr.split(":")[0])
        print("更新代理中...%s" % self.proxyaddr.split(":")[0])
        self.proxyaddr = self.proxy_provider.get_addr()
        self.proxy = {
            'http': 'http://' + self.proxyaddr,
            'https': 'https://' + self.proxyaddr,
        }


# opener = MyOpener()
#
# crawer = ShortComment_Crawer("大象席地而坐", 27172891, opener, 17892, None)
# crawer.craw()

# s = requests.Session()
# s.headers.update(headers)
# openner = MyOpener(s)
#
#
#

#opener = MyOpener(s)
# crawer = ShortComment_Crawer("大象席地而坐", 27172891, 17892, None, request_session=s)
# crawer.craw()
#craw_comment_list(27605698,"西红柿首富", 3300, None)
#craw_movie_id("犯罪", None, None, None, None)
#response = opener.open("https://www.baidu.com")
# print(response.status_code)
# print(response.text)
#
# import queue
#
# q = queue.Queue(20)
# for i in  range(10):
#     q.put(20, block=False)
# print(q.qsize())
# q.get(block=False)
# print(q.qsize())

