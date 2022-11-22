
from flask.helpers import make_response, abort

from entity.sql.base import db
from entity.sql.book_copy import BookCopy

from entity.sql.schemas import book_copy_schema, book_copies_schema


def get_all():
    book_copies = BookCopy.query.all()
    return book_copies_schema.dump(book_copies)


def get(id):
    book_copy = BookCopy.query.filter(BookCopy.id == id).one_or_none()
    if book_copy is not None:
        return book_copy_schema.dump(book_copy)
    else:
        abort(404, f"Book copy with id \"{id}\" not found.")


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
        return book_schema.dump(existing_book_copy), 201
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
