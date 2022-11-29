from flask.helpers import make_response, abort
from mongoengine.errors import DoesNotExist

from entity.sql.base import db
from entity.sql.category import Category
from entity.sql.schemas import category_schema, categories_schema

from entity.nosql.category import Category as MongoCategory
from entity.nosql.schemas_mongo import category_schema as mongo_category_schema
from entity.nosql.schemas_mongo import categories_schema as mongo_categories_schema

from controllers import producer
from apache_kafka.enums import KafkaKey, KafkaTopic


def get_all():
    # Get all categories from mongo database
    categories = MongoCategory.objects
    return mongo_categories_schema.dump(categories)


def get(id):
    # Get one category from mongo database
    try:
        category = MongoCategory.objects.get(id=id)
    except DoesNotExist:
        abort(404, f"Category with id {id} not found.")

    return mongo_category_schema.dump(category)


def create(category):
    new_category = category_schema.load(category, session=db.session)
    db.session.add(new_category)
    db.session.commit()

    producer.send(KafkaTopic.CATEGORY.value, key=KafkaKey.CREATE.value, value=category_schema.dump(new_category))

    return category_schema.dump(new_category), 201


def update(id, category):
    existing_category = Category.query.filter(Category.id == id).one_or_none()

    if not existing_category:
        abort(404, f"Category with id {id} not found.")

    update_category = category_schema.load(category, session=db.session, instance=existing_category)
    db.session.merge(update_category)
    db.session.commit()

    producer.send(KafkaTopic.CATEGORY.value, key=KafkaKey.UPDATE.value, value=category_schema.dump(update_category))

    return category_schema.dump(update_category), 200


def delete(id):
    existing_category = Category.query.filter(Category.id == id).one_or_none()

    if not existing_category:
        abort(404, f"Category with id {id} not found.")

    db.session.delete(existing_category)
    db.session.commit()

    producer.send(KafkaTopic.CATEGORY.value, key=KafkaKey.DELETE.value, value=category_schema.dump({"id": int(id)}))

    return make_response(f"Category with id {id} successfully deleted.", 200)
