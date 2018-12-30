from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from db.model import Base

engine = create_engine('mysql+pymysql://root:password@39.108.123.85:3306/ww?charset=utf8mb4')

Base.metadata.create_all(engine)


session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


