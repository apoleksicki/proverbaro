from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proverbaro.db'
db = SQLAlchemy(app)


class Proverb(db.Model):
    __tablename__ = "Proverbs"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Unicode, nullable=False)
    shown_times = db.Column(db.Integer, default=0, nullable=False)
    shown_last_time = db.Column(db.DateTime, default=None)


@app.route('/')
def hello_world():
    return Proverb.query.order_by(desc(Proverb.shown_last_time)).first().text


if __name__ == '__main__':
    app.run()
