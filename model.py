from sqlalchemy import desc, and_, between, Column, \
    Integer, Date, ForeignKey, Unicode, DateTime
from sqlalchemy.orm import Session, relationship

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
    
    class WordDefinition(Base):
        __tablename__ = 'Word_Definitions'
        id = Column(Integer, primary_key=True)
        word = Column(Unicode, nullable=False)
        definiton = Column(Unicode, nullable=False)        

    class Model(object):
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

    return Model()        
