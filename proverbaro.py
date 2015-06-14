# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, Unicode, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, relationship
from sqlalchemy import create_engine
from sqlalchemy import func
from sqlite3 import dbapi2 as sqlite
from birdy.twitter import UserClient
import datetime
import sys
import traceback
import logging

e = create_engine('sqlite+pysqlite:///proverbaro.db',
                  module=sqlite,
                  encoding="utf-8")

logger = logging.getLogger(__name__)

Base = declarative_base()


class TwitterPublisher(object):
    def __init__(self, consumer_key, consumer_secret, access_token,
                 access_token_key, hashtag):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_key = access_token_key
        self.hashtag = hashtag

    def post_tweet(self, proverb):
        client = UserClient(self.consumer_key, self.consumer_secret,
                            self.access_token, self.access_token_key)
        return client.api.statuses.update.post(status='%s #%s' %\
         (proverb, self.hashtag))


class WordDefinition(Base):
    __tablename__ = 'Word_Definitions'
    id = Column(Integer, primary_key=True)
    word = Column(Unicode, nullable=False)
    definiton = Column(Unicode, nullable=False)

class ProverbToWord(Base):
    __tablename__ = 'Proverbs_To_Words'
    id = Column(Integer, primary_key = True)
    proverb_id = Column(Integer, ForeignKey('Proverbs.id'), nullable=False)
    definition_id = Column(Integer, ForeignKey('Word_Definitions.id'),\
        nullable=False)


class Proverb(Base):
    __tablename__ = 'Proverbs'
    id = Column(Integer, primary_key=True)
    text = Column(Unicode, nullable=False)
    shown_times = Column(Integer, default=0, nullable=False)
    shown_last_time = Column(DateTime, default=None)
    definitions = relationship('WordDefinition', secondary=ProverbToWord)


class PostId(Base):
    __tablename__ = 'Post_Ids'
    id = Column(Integer, primary_key=True)
    publish_date = Column(Date, nullable=False)
    publish_id = Column(Integer, nullable=False)
    proverb_id = Column(Integer, ForeignKey('Proverbs.id'), nullable=False)

    def __init__(self, publish_date, publish_id, proverb_id):
        self.publish_date = publish_date
        self.publish_id = publish_id
        self.proverb_id = proverb_id

def create_tables():
    Base.metadata.create_all(e)


def _calculate_publish_id(date, session):
    currentId = session.query(func.max(PostId.publish_id)).filter(
        PostId.publish_date == date).first()[0]
    if currentId is None:
        currentId = 1
    else:
        currentId += 1
    return currentId


def _create_PostId(session, proverbId):
    today = datetime.date.today()
    publishId = _calculate_publish_id(today, session)
    return PostId(today, publishId, proverbId)


def fetch_next_proverb(session):
    return session.query(Proverb).filter(
        Proverb.shown_times == session.query(
            func.min(Proverb.shown_times))).order_by(func.random()).first()


def _fetch_last_post_date(session):
    return session.query(func.max(Proverb.shown_last_time)).first()[0]


def fetch_delta_from_last_post():
    session = Session(bind=e)
    try:
        lastpost = _fetch_last_post_date(session)
        if lastpost is not None:
            delta = datetime.datetime.today() - lastpost
            logger.warning('Last post was %d seconds ago',
                           delta.total_seconds())
            return delta.total_seconds()
        else:
            logger.warning('First run, no posts have been shown')
            return None
    except:
        logger.exception('Exception while posting', exc_info=True)
        session.rollback()
    finally:
        session.close()


def show_proverb(publisher):
    session = Session(bind=e)
    try:
        proverb = fetch_next_proverb(session)
        proverb.shown_times += 1
        proverb.shown_last_time = datetime.datetime.now()
        publisher.post_tweet(proverb.text)
        session.add(_create_PostId(session, proverb.id))
        session.commit()
        logger.warning(proverb.text.encode("utf-8").rstrip())
    except:
        traceback.print_exc(file=sys.stdout)
        logger.exception('Exception while posting', exc_info=True)
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    create_tables()        
