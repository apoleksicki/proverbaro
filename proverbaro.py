# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlite3 import dbapi2 as sqlite
from random import shuffle

e = create_engine('sqlite+pysqlite:///proverbaro.db', module=sqlite, encoding="utf-8")
Base = declarative_base()

class Proverb(Base):
    __tablename__ = "Proverbs"
    id = Column(Integer, primary_key=True)
    text = Column(Unicode, nullable=False)
    shown_times = Column(Integer, default=0, nullable=False)

s = Session(bind=e)

def find_min_shown_times():
    return s.query(func.min(Proverb.shown_times))

def get_proverbs():
    s = Session(bind=e)
    proverbs = s.query(Proverb).filter(Proverb.shown_times == s.query(func.min(Proverb.shown_times))).all()
    shuffle(proverbs)
    return proverbs

proverbs = get_proverbs()
len(proverbs)

def print_all_proverbs():
    s = Session(bind=e)
    for p in s.query(Proverb).all():
        print p.shown_times, p.text.encode("utf-8")

print_all_proverbs()

if __name__ == '__main__':
    for p in s.query(Proverb).all():
        print p.shown_times, p.text.encode("utf-8")
