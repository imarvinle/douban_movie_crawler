# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
-------------------------------------------------
   Description :  配置文件, 主要是数据库和线程数配置
   Author :       lichunlin
   date：          2018/12/31
-------------------------------------------------
'''

# Configure the database information
DIALECT = 'mysql'               # 使用的数据库
DRIVER = 'pymysql'              # 驱动 可选: pymysql、 mysqlconnector
USERNAME = 'root'
PASSWORD = 'password'
HOST = '39.108.123.85'
PORT = '3306'
DATABASE = 'doubanmovie'             # 数据库名
DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)


# Configure the thread info
TagThreadSize = 0
MovieThreadSize = 0
ShortCommentSize = 2
CommentSize = 2
DataBaseInsertSize = 4
