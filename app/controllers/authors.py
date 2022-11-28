from flask.helpers import make_response, abort
from mongoengine.errors import DoesNotExist

from entity.sql.base import db
from entity.sql.author import Author
from entity.sql.book import Book
from entity.sql.schemas import author_schema, authors_schema

from entity.nosql.author import Author as AuthorMongo
from entity.nosql.schemas_mongo import author_schema as mongo_author_schema
from entity.nosql.schemas_mongo import authors_schema as mongo_authors_schema

from controllers import producer
from apache_kafka.enums import KafkaKey, KafkaTopic


def get_all():
    # Get all authors from mongo database
    authors_mongo = AuthorMongo.objects
    return mongo_authors_schema.dump(authors_mongo)


def get(id):
    # Get one author from mongo database
    try:
        author = AuthorMongo.objects.get(id=int(id))
    except DoesNotExist:
        abort(404, f"Author with id {id} not found.")

    return mongo_author_schema.dump(author)


def create(author):
    # create author and make a commit to SQL database
    new_author = author_schema.load(author, session=db.session)
    db.session.add(new_author)
    db.session.commit()

    # create this author in Mongo database as well
    producer.send(KafkaTopic.AUTHOR.value, key=KafkaKey.CREATE.value, value=author_schema.dump(new_author))

    return author_schema.dump(new_author), 201


def update(id, author):
    existing_author = Author.query.filter(Author.id == id).one_or_none()
    if not existing_author:
        abort(404, f"Author with id {id} not found.")

    update_author = author_schema.load(author, session=db.session, instance=existing_author)
    db.session.merge(update_author)
    db.session.commit()

    # send updated author to Mongo database
    producer.send(KafkaTopic.AUTHOR.value, key=KafkaKey.UPDATE.value, value=author_schema.dump(update_author))

    return author_schema.dump(update_author), 200


def delete(id):
    existing_author = Author.query.filter(Author.id == id).one_or_none()
    if not existing_author:
        abort(404, f"Author with id \"{id}\" not found.")

    db.session.delete(existing_author)
    db.session.commit()

    # send author delete request to Mongo database
    producer.send(KafkaTopic.AUTHOR.value, key=KafkaKey.DELETE.value, value={"id": int(id)})

    return make_response(f"Author with id {id} successfully deleted.", 200)
