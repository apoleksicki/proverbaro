from sqlalchemy import desc, and_, between, Column, \
    Integer, Date, ForeignKey, Unicode, DateTime
from sqlalchemy.orm import Session, relationship
from sqlalchemy import func
from sqlalchemy import Column, Integer, Unicode, DateTime, Date, ForeignKey
import datetime

global proverb_to_show

def init_model(Base):

    class PostId(Base):
        __tablename__ = 'Post_Ids'
        id = Column(Integer, primary_key=True)
        publish_date = Column(Date, nullable=False)
        publish_id = Column(Integer, nullable=False)
        proverb_id = Column(Integer, ForeignKey('Proverbs.id'),
                               nullable=False)

        def __init__(self, publish_date, publish_id, proverb_id):
            self.publish_date = publish_date
            self.publish_id = publish_id
            self.proverb_id = proverb_id


    class Proverb(Base):
        __tablename__ = "Proverbs"
        id = Column(Integer, primary_key=True)
        text = Column(Unicode, nullable=False)
        shown_times = Column(Integer, default=0, nullable=False)
        shown_last_time = Column(DateTime, default=None)
        posts = relationship(PostId, backref='Proverb')


    class ProverbToWord(Base):
        __tablename__ = 'Proverbs_To_Words'
        left_id = Column('proverb_id', Integer,\
            ForeignKey('Proverbs.id'), primary_key=True)
        right_id = Column('definition_id', Integer,\
            ForeignKey('Word_Definitions.id'), primary_key=True)
        proverb = relationship('Proverb')
        

    class WordDefinition(Base):
        __tablename__ = 'Word_Definitions'
        id = Column(Integer, primary_key=True)
        word = Column(Unicode, nullable=False)
        definiton = Column(Unicode, nullable=False)


    class Repository(object):
        def proverb_to_show(self, date, publish_id):
            return Proverb.query.join(PostId).filter(and_(
                PostId.publish_date == date,
                PostId.publish_id == publish_id)).first()
        def latest_post_id(self):
            return PostId.query.order_by(desc(PostId.publish_date),\
                desc(PostId.publish_id)).first()   
        def post_list(self, fromDate, toDate):
            return PostId.query.filter(between(PostId.publish_date,\
                fromDate, toDate)).order_by(desc(PostId.publish_date),\
                PostId.publish_id).all()
        def calculate_publish_id(self, date, session):
            return session.query(func.max(PostId.publish_id)).\
                filter(PostId.publish_date == date).first()[0]

        def _calculate_publish_id(self, date, session):
            currentId = self.calculate_publish_id(date, session)
            if currentId is None:
                currentId = 1
            else:
                currentId += 1
            return currentId

        def create_PostId(self, session, proverbId):
            today = datetime.date.today()
            publishId = self._calculate_publish_id(today, session)
            return PostId(today, publishId, proverbId)
        
        def fetch_next_proverb(self, session):
            return session.query(Proverb).filter(
                Proverb.shown_times == session.query(
                    func.min(Proverb.shown_times)))\
                    .order_by(func.random()).first()

        def fetch_last_post_date(self, session):
            return session.query(func.max(Proverb.shown_last_time)).first()[0]            



    return Repository()        
