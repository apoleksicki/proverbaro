# -*- coding: utf-8 -*-
# from sqlalchemy import Column, Integer, Unicode, DateTime, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session  # , relationship
from sqlalchemy import create_engine

from sqlite3 import dbapi2 as sqlite
from birdy.twitter import UserClient
from model import init_model
import datetime
import sys
import traceback
import logging

e = create_engine(
    'sqlite+pysqlite:///proverbaro.db',
    module=sqlite,
    encoding="utf-8",
)

logger = logging.getLogger(__name__)

Base = declarative_base()

repository = init_model(Base)


class TwitterPublisher(object):
    def __init__(
            self, consumer_key, consumer_secret, access_token,
            access_token_key, hashtag):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_key = access_token_key
        self.hashtag = hashtag

    def post_tweet(self, proverb):
        client = UserClient(self.consumer_key, self.consumer_secret,
                            self.access_token, self.access_token_key)
        return client.api.statuses.update.post(
            status='%s #%s' % (proverb, self.hashtag))


def create_tables():
    Base.metadata.create_all(e)


def fetch_delta_from_last_post():
    session = Session(bind=e)
    try:
        lastpost = repository.fetch_last_post_date(session)
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


def fetch_proverb():
    session = Session(bind=e)
    try:
        repository.fetch_next_proverb(session)
    finally:
        session.close()


def show_proverb(publisher):
    session = Session(bind=e)
    try:
        proverb = repository.fetch_next_proverb(session)
        proverb.shown_times += 1
        proverb.shown_last_time = datetime.datetime.now()
        publisher.post_tweet(proverb.text)
        session.add(repository.create_PostId(session, proverb.id))
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
