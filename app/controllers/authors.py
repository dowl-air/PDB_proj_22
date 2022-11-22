from flask.helpers import make_response, abort

from entity.sql.base import db
from entity.sql.author import Author

from entity.sql.schemas import author_schema, authors_schema


def get_all():
    authors = Author.query.all()
    return authors_schema.dump(authors)


def get(id):
    author = Author.query.filter(Author.id == id).one_or_none()
    if author is not None:
        return author_schema.dump(author)
    else:
        abort(404, f"Author with id \"{id}\" not found.")


def create(author):
    new_author = author_schema.load(author, session=db.session)
    db.session.add(new_author)
    db.session.commit()
    return author_schema.dump(new_author), 201


def update(id, author):
    existing_author = Author.query.filter(Author.id == id).one_or_none()

    if existing_author:
        update_author = author_schema.load(author, session=db.session, instance=existing_author)
        db.session.merge(update_author)
        db.session.commit()
        return author_schema.dump(existing_author), 201
    else:
        abort(404, f"Author with id \"{id}\" not found.")


def delete(id):
    existing_author = Author.query.filter(Author.id == id).one_or_none()

    if existing_author:
        db.session.delete(existing_author)
        db.session.commit()
        return make_response(f"Author with id \"{id}\" successfully deleted.", 200)
    else:
        abort(404, f"Author with id \"{id}\" not found.")
