# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlite3 import dbapi2 as sqlite
from random import shuffle
import sys

e = create_engine('sqlite+pysqlite:///proverbaro.db', module=sqlite, encoding="utf-8")
Base = declarative_base()

class Proverb(Base):
    __tablename__ = "Proverbs"
    id = Column(Integer, primary_key=True)
    text = Column(Unicode, nullable=False)
    shown_times = Column(Integer, default=0, nullable=False)

def fetch_next_proverb(session):
    return session.query(Proverb).filter(Proverb.shown_times == s.query(func.min(Proverb.shown_times))).order_by(func.random()).first()

def show_proverb():
        session = Session(bind=e)
        try:
            proverb = fetch_next_proverb(session)
            proverb.shown_times += 1
            session.commit()
            print proverb.text.encode("utf-8")
        except:
            print sys.exc_info()
            session.rollback()
        finally:
            session.close()

if __name__ == '__main__':
    show_proverb()
