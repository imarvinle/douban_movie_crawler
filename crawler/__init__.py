# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
-------------------------------------------------
   Description :  简单封装网络请求，后期可支持扩展代理，随机化请求头，定期更换cookies
   Author :       lichunlin
   date：          2018/12/31
-------------------------------------------------
'''

import random
import requests

user_agent = [
    "Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729;.NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
]

headers = {
        "User-Agent": random.choice(user_agent),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "movie.douban.com",
        "Referer": "https://movie.douban.com",
        'Connection': 'keep-alive'
}

def get_session():
    request_session = requests.Session()
    headers["User-Agent"] = random.choice(user_agent)
    request_session.headers.update(headers)
    return request_session

class MyOpener():

    def __init__(self, taskname):
        self.taskname = taskname
        self.session = get_session()
        self.requst_count = 0
        self.retry_count = 0
        self.exception_count = 0

    def open(self, req):
        while True:
            try:
                response = self.session.get(req)
                self.requst_count = self.requst_count + 1
                if self.requst_count % 20 == 0:
                    self.session = get_session()

                if response.status_code != 200:
                    self.session = get_session()
                    self.requst_count = self.retry_count + 1
                    if self.retry_count > 3:
                        print("[Opener-%s] 多次重试还是返回statu_code:[%d] " % (self.taskname, response.status_code))
                        return {"result": False, "data": None}
                    continue
                self.retry_count = 0
                return {"result": True, "data": response}
            except Exception as e:
                print("[Opener-%s] 出现异常 " % self.taskname)
                self.session = get_session()
                self.exception_count = self.exception_count + 1
                if self.exception_count > 3:
                    print("[Opener-%s] 多次出现异常" % (self.taskname))
                    return {"result": False, "data": None}

#   取消模拟登陆
# def Login():
#     login_url = 'https://accounts.douban.com/login?source=movie'
#     form_data = {
#         "form_email": "17738729175",
#         "form_password": "******",
#         "source": "movie",
#         "redir": "https://movie.douban.com/",
#         "login": "登录"
#     }
#     request_session = get_session()
#
#     html = request_session.get(login_url).text
#     soup = BeautifulSoup(html, "html.parser")
#     if soup.find('img', id='captcha_image'):
#         print("有验证码")
#         # 获取验证码图片地址
#         captcha_url = soup.find('img', id='captcha_image')['src']
#         # 匹配验证码id
#         reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
#         captchaID = re.findall(reCaptchaID, html)
#         # 下载验证码图片
#         resp_img = request_session.get(captcha_url).content
#         with open("captcha.jpg", "wb") as file:
#             file.write(resp_img)
#         img = pyplot.imread("captcha.jpg")
#         pyplot.imshow(img)
#         pyplot.axis('off')
#         pyplot.show()
#         # 输入验证码并加入提交信息中，重新编码提交获得页面内容
#         captcha = input('please input the captcha:')
#         form_data['captcha-solution'] = captcha
#         form_data['captcha-id'] = captchaID[0]
#         login_url= 'https://accounts.douban.com/login'
#
#         login_success = request_session.post(login_url, data=form_data)
#         print(request_session.cookies)
#         print("登陆成功<%d>" % login_success.status_code)
#         return request_session
#     else:
#         print("未登陆")
#         return None


if __name__ == "__main__":
    pass