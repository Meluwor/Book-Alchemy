import os

from data_models import db, Author, Book
from flask import Flask

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)