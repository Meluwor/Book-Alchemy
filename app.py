from datetime import datetime
import os

from sqlalchemy import or_

from data_models import db, Author, Book
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_cors import CORS

app = Flask(__name__)

# Some key is needed to activate flash
app.secret_key = 'some_key'

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)


@app.route('/home', methods=['GET', 'POST'])
def home():
    """
    This route handles the homepage.
    """
    search_for = request.args.get('search')
    if search_for:
        query = Book.query.join(Author)
        search_for = f"%{search_for}%"
        query = query.filter(
            or_(
                Book.title.like(search_for),
                Author.name.like(search_for)
            )
        )
        result = query.all()
        return render_template("home.html", books=result)

    sort_by = request.args.get('sort_by', 'title')
    if sort_by:
        if sort_by == 'author':
            books = Book.query.join(Author).order_by(Author.name).all()
        else:
            books = Book.query.order_by(Book.title).all()
    else:
        books = Book.query.all()
    return render_template("home.html", books=books)


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

        db.session.add(new_author)
        db.session.commit()
        # TODO user needs/wants more info
        return redirect(url_for('home'))


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    This route handles the creation of a book.
    """
    if request.method == 'GET':
        authors = Author.query.all()
        return render_template("add_book.html", authors=authors)
    else:
        title = request.form.get('title')
        author_id = request.form.get('author_id')
        isbn = request.form.get('isbn')
        publication_year = request.form.get('publication_year')
        publication_year = get_date(publication_year)

        new_book = Book()
        new_book.title = title
        new_book.author_id = author_id
        new_book.isbn = isbn
        new_book.publication_year = publication_year

        db.session.add(new_book)
        db.session.commit()
        # TODO user needs/wants more info
        return redirect(url_for('home'))


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    This route will delete a book.
    """
    book = Book.query.get(book_id)
    if not book:
        flash(f'Book_id:{book_id} does not exist.', 'info')
        return redirect(url_for('home'))
    author_id = book.author_id
    try:

        db.session.delete(book)
        db.session.commit()
        check_author(author_id)

        flash(f'{book.title} deleted.', 'success')
        return redirect(url_for('home'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error while deleting book_id:{book_id}.', 'danger')
        return redirect(url_for('home'))


def check_author(author_id):
    """
    This function will delete an author if there are no more books of this author.
    """
    books_count = Book.query.filter_by(author_id=author_id).count()
    if books_count == 0:
        author = Author.query.get(author_id)
        if author:
            db.session.delete(author)
            db.session.commit()
            flash(f'Author {author.name} was also deleted because they have no more books.',
                  'info')


def get_date(date_string: str):
    """
    This function shall return a given string(date) as a date.
    """
    if date_string:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)

# with app.app_context():
#   db.create_all()
