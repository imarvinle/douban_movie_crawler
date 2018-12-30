# -*- coding: utf-8 -*-

# cookies处理

# 编码信息，生成请求，打开页面获取内容
from bs4 import BeautifulSoup

from crawers import MyOpener


def craw_shortcomment(movie_name, movie_id, shortcomnum, db_queue):
    shortcomment_craw = ShortComment_Crawer(movie_name, movie_id, shortcomnum, db_queue)
    shortcomment_craw.craw()


class ShortComment_Crawer():

    def __init__(self, movie_name, movie_id, shortcomnum, db_queue, opener=None):
        self.movie_id = movie_id
        self.movie_name = movie_name
        self.shortcomnum = shortcomnum
        self.pagenum = self.shortcomnum // 20
        self.db_queue = db_queue
        self.opener = opener
        if not self.opener:
            self.opener = MyOpener("[%s]短评" % movie_name)

        if self.shortcomnum % 20 > 0:
            self.pagenum = self.pagenum + 1

        self.content = ""
        self.nickname = ""
        self.likenum = 0
        self.time = ""

    def saveFile(self, list):
        with open("duanping.txt", "a") as file:
            for item in list:
                file.write(str(item))
                file.write("\n")

    def craw(self):
        comment_list = []
        for page in range(self.pagenum):
            print("********** 正在爬取电影 <%s> 的第 %d 页的短评 **********\n" % (self.movie_name, page + 1))

            url = 'https://movie.douban.com/subject/' + str(self.movie_id)+'/comments?start=' + str(page*20) + '&limit=20&sort=new_score&status=P'

            res = self.opener.open(url)

            if not res["result"]:
                print("停止爬取 <%s> 短评\n" % (self.movie_name))
                if len(comment_list) > 0:
                    self.saveFile(comment_list)
                    #self.db_queue.put((db_operate, [], {"value": comment_list, "type": "short"}))
                break
            html = res["data"].text
            soup = BeautifulSoup(html, "html.parser")
            comment_items = soup.select("div.comment-item")
            for item in comment_items:
                self.content = item.select("div.comment > p")[0].get_text().split()[0]
                print(self.content)
                self.nickname = item.select("div.avatar > a")[0]["title"].split()[0]
                self.likenum = int(item.select("span.votes")[0].get_text().split()[0])
                self.time = item.select("span.comment-time ")[0].get_text().split()[0]
                #comment_list.append(ShortComment(self.movie_name, self.nickname, self.time, self.content, self.likenum))
                comment_list.append("%s %s %d %s" % (self.content, self.nickname, self.likenum, self.time))
            if (page+1) % 4 == 0:
                #self.db_queue.put((db_operate, [], {"value": comment_list, "type": "short"}))
                self.saveFile(comment_list)
                comment_list.clear()
        if len(comment_list) != 0:
            #self.db_queue.put((db_operate, [], {"value": comment_list, "type": "short"}))
            self.saveFile(comment_list)


if __name__ == "__main__":
    pass