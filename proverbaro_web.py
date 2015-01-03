from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc, and_

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

    def __init__(self, publish_date, publish_id, proverb_id):
        self.publish_date = publish_date
        self.publish_id = publish_id
        self.proverb_id = proverb_id

    id = db.Column(db.Integer, primary_key=True)
    publish_date = db.Column(db.Date, nullable=False)
    publish_id = db.Column(db.Integer, nullable=False)
    proverb_id = db.Column(db.Integer, db.ForeignKey('Proverbs.id'),
                           nullable=False)


@app.route('/<date>/<int:publish_id>')
def show_proverb(date, publish_id):
    return Proverb.query.join(PostId).filter(and_(
            PostId.publish_date == date,
            PostId.publish_id == publish_id)).first().text

if __name__ == '__main__':
    app.run(debug=True)
