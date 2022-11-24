
from flask.helpers import make_response, abort
from mongoengine.errors import DoesNotExist

from entity.sql.base import db
from entity.sql.book import Book
from entity.sql.schemas import book_schema, books_schema

from entity.nosql.book import Book as MongoBook
from entity.nosql.schemas_mongo import book_schema as mongo_book_schema
from entity.nosql.schemas_mongo import books_schema as mongo_books_schema


def get_all():
    # Get all authors from mongo database
    books = MongoBook.objects
    return mongo_books_schema.dump(books)


def get(id):
    # Get one author from mongo database
    try:
        book = MongoBook.objects.get(id=id)
    except DoesNotExist:
        abort(404, f"Book with id {id} not found.")

    return mongo_book_schema.dump(book)


def create(book):
    ISBN = book.get("ISBN")
    existing_book = Book.query.filter(Book.ISBN == ISBN).one_or_none()

    if existing_book is None:
        new_book = book_schema.load(book, session=db.session)
        db.session.add(new_book)
        db.session.commit()
        return book_schema.dump(new_book), 201
    else:
        abort(406, f"Book with ISBN {ISBN} already exists.")


def update(id, book):
    existing_book = Book.query.filter(Book.id == id).one_or_none()

    if existing_book:
        update_book = book_schema.load(book, session=db.session, instance=existing_book)
        db.session.merge(update_book)
        db.session.commit()
        return book_schema.dump(existing_book), 200
    else:
        abort(404, f"Book with id \"{id}\" not found.")


def delete(id):
    existing_book = Book.query.filter(Book.id == id).one_or_none()

    if existing_book:
        db.session.delete(existing_book)
        db.session.commit()
        return make_response(f"Book with id \"{id}\" successfully deleted.", 200)
    else:
        abort(404, f"Book with id \"{id}\" not found.")
