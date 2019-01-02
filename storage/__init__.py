# -*- coding: utf-8 -*-
# !/usr/bin/env python

'''
-------------------------------------------------
   Description :  数据库初始化、会话管理
   Author :       lichunlin
   date：          2018/12/31
-------------------------------------------------
'''


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from storage.model import Base
from config import DATABASE_URI, DataBaseInsertSize

engine = create_engine(DATABASE_URI)

Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


