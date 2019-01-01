#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import  os

# config for sqlalchemy
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'password'
HOST = '39.108.123.85'
PORT = '3306'
DATABASE = 'doubanmovie'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)
#设置禁用追踪对对象的修改并发送信号
SQLALCHEMY_TRACK_MODIFICATIONS = False
#yes启动自动提交数据库更改在每个请求
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
