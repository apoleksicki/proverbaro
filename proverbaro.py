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

session = Session(bind=e)
proverbs_query = session.query(Proverb).filter(Proverb.shown_times == s.query(func.min(Proverb.shown_times))).order_by(func.random())
proverbs_query
proverb = proverbs_query.first()
proverb.text

def mark_as_shown(session, proverb):
    proverb.id += 1
    session.add(proverb)

def show_proverbs(proverbs):
    for proverb in proverbs:
        session = Session(bind=e)
        try:
            mark_as_shown(session, proverb)
            session.commit()
        except:
            session.rollback()
        finally:
            session.close()
        print proverb.text.encode("utf-8")

def main_loop():
    session = Session(bind=e)
    proberbs = None
    try:
        proverbs = get_proverbs(session, True)
    finally:
        session.close()
    show_proverbs(proverbs)

main_loop()

def print_all_proverbs():
    for p in get_proverbs(Session(bind=e), debug=True):
        print p.shown_times, p.text.encode("utf-8")

print_all_proverbs()

if __name__ == '__main__':
    for p in s.query(Proverb).all():
        print p.shown_times, p.text.encode("utf-8")
