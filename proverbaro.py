# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Unicode, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlite3 import dbapi2 as sqlite
from random import shuffle
from birdy.twitter import UserClient
from datetime import datetime

import sys, traceback, logging

e = create_engine('sqlite+pysqlite:///proverbaro.db', module=sqlite, encoding="utf-8")

logger = logging.getLogger(__name__)

Base = declarative_base()

class TwitterPublisher(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_key):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_key = access_token_key
    def post_tweet(self, proverb):
        client = UserClient(self.consumer_key, self.consumer_secret, self.access_token, self.access_token_key)
        return client.api.statuses.update.post(status=proverb)

class Proverb(Base):
    __tablename__ = "Proverbs"
    id = Column(Integer, primary_key=True)
    text = Column(Unicode, nullable=False)
    shown_times = Column(Integer, default=0, nullable=False)
    shown_last_time = Column(DateTime, default=None)

def fetch_next_proverb(session):
    return session.query(Proverb).filter(Proverb.shown_times == session.query(func.min(Proverb.shown_times))).order_by(func.random()).first()

def show_proverb(publisher):
        session = Session(bind=e)
        try:
            proverb = fetch_next_proverb(session)
            proverb.shown_times += 1
            proverb.shown_last_time = datetime.now()
            publisher.post_tweet(proverb.text)
            session.commit()
            logger.warning(proverb.text.encode("utf-8").rstrip())
        except:
            traceback.print_exc(file=sys.stdout)
            logger.exception('Exception while posting', exc_info=True)

            session.rollback()
        finally:
            session.close()
