
from flask.helpers import make_response, abort
from mongoengine.errors import DoesNotExist

from entity.sql.base import db
from entity.sql.book_copy import BookCopy
from entity.sql.schemas import book_copy_schema, book_copies_schema

from entity.nosql.book_copy import BookCopy as MongoBookCopy
from entity.nosql.schemas_mongo import book_copy_schema as mongo_book_copy_schema
from entity.nosql.schemas_mongo import book_copies_schema as mongo_book_copies_schema


def get_all():
    # Get all book copies from mongo database
    book_copies = MongoBookCopy.objects
    return mongo_book_copies_schema.dump(book_copies)


def get(id):
    # Get one book copy from mongo database
    try:
        book = MongoBookCopy.objects.get(id=id)
    except DoesNotExist:
        abort(404, f"Book copy with id {id} not found.")

    return mongo_book_copy_schema.dump(book)


def create(book_copy):
    new_book_copy = book_copy_schema.load(book_copy, session=db.session)
    db.session.add(new_book_copy)
    db.session.commit()
    return book_copy_schema.dump(new_book_copy), 201


def update(id, book_copy):
    existing_book_copy = BookCopy.query.filter(BookCopy.id == id).one_or_none()

    if existing_book_copy:
        update_book_copy = book_copy_schema.load(book_copy, session=db.session, instance=existing_book_copy)
        db.session.merge(update_book_copy)
        db.session.commit()
        return book_copy_schema.dump(existing_book_copy), 200
    else:
        abort(404, f"Book copy with id \"{id}\" not found.")


def delete(id):
    existing_book_copy = BookCopy.query.filter(BookCopy.id == id).one_or_none()

    if existing_book_copy:
        db.session.delete(existing_book_copy)
        db.session.commit()
        return make_response(f"Book copy with id \"{id}\" successfully deleted.", 200)
    else:
        abort(404, f"Book copy with id \"{id}\" not found.")
