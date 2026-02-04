from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Author(db.Model):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    books = relationship("Book", back_populates="author")
    def __repr__(self):
        """
        A simple info string if needed.
        """
        return f"<Author id: {self.id}, name: '{self.name}')>"


    def __str__(self):
        """
        A simple info string if needed.
        """
        birth = self.birth_date.year if self.birth_date else "unknown"
        death = self.date_of_death.year if self.date_of_death else "unknown"
        return f"Author: {self.name} birth_date: {birth} date_of_death: {death}"

class Book(db.Model):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    isbn = Column(Integer)
    title = Column(String)
    publication_year = Column(Date)

    author = relationship("Author", back_populates="books")

    def __repr__(self):
        """
        A simple info string if needed.
        """
        return f"<Book id: {self.id}, title: '{self.title}')>"

    def __str__(self):
        """
        A simple info string if needed.
        """
        return f"<Book id: {self.id}, title: '{self.title}')>"

def main():
    print("start")


if __name__ == "__main__":
    main()
