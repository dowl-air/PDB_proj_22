from flask.helpers import make_response, abort
from mongoengine.errors import DoesNotExist

from entity.sql.base import db
from entity.sql.author import Author
from entity.sql.schemas import author_schema, authors_schema

from entity.nosql.author import Author as AuthorMongo
from entity.nosql.schemas_mongo import author_schema as mongo_author_schema
from entity.nosql.schemas_mongo import authors_schema as mongo_authors_schema

from controllers import producer
from apache_kafka.enums import KafkaKey, KafkaTopic


def get_all():
    # Get all authors from mongo database
    authors_mongo = AuthorMongo.objects

    # TEST kafka broker
    # todo remove
    obj = {
        "test": "test"
    }
    producer.send("global", key=KafkaKey.CREATE, value=obj)

    return mongo_authors_schema.dump(authors_mongo)


def get(id):
    # Get one author from mongo database
    try:
        author = AuthorMongo.objects.get(id=id)
    except DoesNotExist:
        abort(404, f"Author with id {id} not found.")

    # TEST kafka broker
    # todo remove
    producer.send(KafkaTopic.AUTHOR, key=KafkaKey.CREATE, value={"test": "test_string"})

    return mongo_author_schema.dump(author)


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
        return author_schema.dump(existing_author), 200
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
