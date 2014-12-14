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

def get_proverbs(session, debug=False):
    proverbs_query = session.query(Proverb).filter(Proverb.shown_times == s.query(func.min(Proverb.shown_times)))
    if debug:
        proverbs_query = proverbs_query.limit(10)
    proverbs = proverbs_query.all()
    shuffle(proverbs)
    return proverbs

def mark_as_shown(proverb):
    pass


def print_all_proverbs():
    for p in get_proverbs(Session(bind=e), debug=True):
        print p.shown_times, p.text.encode("utf-8")

if __name__ == '__main__':
    for p in s.query(Proverb).all():
        print p.shown_times, p.text.encode("utf-8")
