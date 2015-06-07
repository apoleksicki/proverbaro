import logging
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc, and_
from translation_util import find_definition

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


class Proverb(db.Model):
    __tablename__ = "Proverbs"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Unicode, nullable=False)
    shown_times = db.Column(db.Integer, default=0, nullable=False)
    shown_last_time = db.Column(db.DateTime, default=None)


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


@app.route('/<date>/<int:publish_id>')
def show_proverb(date, publish_id):
    proverb = Proverb.query.join(PostId).filter(and_(
            PostId.publish_date == date,
            PostId.publish_id == publish_id)).first()
    definition1 = None
    if proverb is not None:
        definition1 = find_definition(proverb.text.split()[0])

    return render_template('proverb.html',
                           proverb=proverb.text
                           if proverb is not None else None,
                          definition=definition1)


@app.route('/')
def function():
    post = PostId.query.order_by(desc(PostId.publish_date), desc(PostId.publish_id)).first()
    return show_proverb(post.publish_date, post.publish_id)   


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
