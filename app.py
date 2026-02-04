from datetime import datetime
import os

from data_models import db, Author, Book
from flask import Flask, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes
basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    This route handles the creation of a new author.
    """
    if request.method == 'GET':
        return render_template("add_author.html")
    else:
        name = request.form.get('name')
        birth_date = request.form.get('birthdate')
        birth_date = get_date(birth_date)
        date_of_death = request.form.get('date_of_death')
        if date_of_death:
            date_of_death = get_date(date_of_death)

        new_author = Author()
        new_author.name = name
        new_author.birth_date = birth_date
        if date_of_death:
            new_author.date_of_death = date_of_death
        print(new_author)
        db.session.add(new_author)
        db.session.commit()
        return render_template("add_author.html")


def get_date(date_string: str):
    """
    This function shall return a given string(date) as a date
    """
    return datetime.strptime(date_string, '%Y-%m-%d').date()


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

# with app.app_context():
#   db.create_all()
