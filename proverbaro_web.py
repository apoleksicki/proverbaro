import logging
from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from translation_util import find_definition, split_proverb_into_words
from collections import OrderedDict
from datetime import timedelta
from model import init_model

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


model = init_model(db.Model)

@app.route('/<date>/<int:publish_id>')
def show_proverb(date, publish_id):
    proverb = model.proverb_to_show(date, publish_id)
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
    return model.latest_post_id()


@app.route('/')
def home():
    latest = _fetch_latest_postId()
    toDate = latest.publish_date
    fromDate = toDate - timedelta(3)
    posts = model.post_list(fromDate, toDate)
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
