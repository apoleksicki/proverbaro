import logging
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc, and_, between
from translation_util import find_definition, split_proverb_into_words
from collections import OrderedDict
from datetime import timedelta

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='proverbaro.log', format=FORMAT)
console = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s: %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proverbaro.db'
db = SQLAlchemy(app)


class PostId(db.Model):
    __tablename__ = 'Post_Ids'
    id = db.Column(db.Integer, primary_key=True)
    publish_date = db.Column(db.Date, nullable=False)
    publish_id = db.Column(db.Integer, nullable=False)
    proverb_id = db.Column(db.Integer, db.ForeignKey('Proverbs.id'),
                           nullable=False)

    def __init__(self, publish_date, publish_id, proverb_id):
        self.publish_date = publish_date
        self.publish_id = publish_id
        self.proverb_id = proverb_id


class Proverb(db.Model):
    __tablename__ = "Proverbs"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Unicode, nullable=False)
    shown_times = db.Column(db.Integer, default=0, nullable=False)
    shown_last_time = db.Column(db.DateTime, default=None)
    posts = db.relationship(PostId, backref='Proverb')


@app.route('/<date>/<int:publish_id>')
def show_proverb(date, publish_id):
    proverb = Proverb.query.join(PostId).filter(and_(
            PostId.publish_date == date,
            PostId.publish_id == publish_id)).first()
    definitions = []
    if proverb is not None:
        definitions = [find_definition(split_proverb_into_words(proverb.text)[0]),
                        find_definition(split_proverb_into_words(proverb.text)[2])]
    print definitions                        
    return render_template('proverb.html',
                           proverb=proverb.text
                           if proverb is not None else None,
                          definitions=definitions)


def _reduce_to_dictionary(dict, post_tuple):
    date = post_tuple[0]
    if not dict.has_key(date):
        dict[date] = []
    dict[date].append(post_tuple[1:])
    return dict


def _fetch_latest_postId():
    return PostId.query.order_by(desc(PostId.publish_date), desc(PostId.publish_id)).first()


@app.route('/')
def home():
    latest = _fetch_latest_postId()
    toDate = latest.publish_date
    fromDate = toDate - timedelta(3)
    posts = PostId.query.filter(between(PostId.publish_date, fromDate, toDate))\
    .order_by(desc(PostId.publish_date), PostId.publish_id).all()
    post_tuples = [(post.publish_date, post.publish_id, post.Proverb.text) for post in posts]
    proverbDictionary = reduce(_reduce_to_dictionary, post_tuples, OrderedDict())
    return render_template('index.html', proverbs = proverbDictionary)   


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()


@app.route('/shutdown')
def shutdown():
    if app.debug:
        shutdown_server()
        return 'Server shutting down...'
    else:
        return 'Cannot shut down, not in debug mode.'        


if __name__ == '__main__':
    app.run(debug=True)
