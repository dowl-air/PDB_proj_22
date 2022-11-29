from flask.helpers import make_response, abort
from mongoengine.errors import DoesNotExist

from entity.sql.base import db
from entity.sql.review import Review
from entity.sql.schemas import review_schema, reviews_schema

from entity.nosql.review import Review as MongoReview
from entity.nosql.schemas_mongo import review_schema as mongo_review_schema
from entity.nosql.schemas_mongo import reviews_schema as mongo_reviews_schema

from controllers import producer
from apache_kafka.enums import KafkaKey, KafkaTopic


def get_all():
    # Get all reviews from mongo database
    reviews = MongoReview.objects
    return mongo_reviews_schema.dump(reviews)


def book_get_all(id):
    # Get all reviews from specified book from mongo database
    reviews = MongoReview.objects(book_id=id)
    return mongo_reviews_schema.dump(reviews)


def get(id):
    # Get one review from mongo database
    try:
        review = MongoReview.objects.get(id=id)
    except DoesNotExist:
        abort(404, f"Review with id {id} not found.")

    return mongo_review_schema.dump(review)


def create(id, review, user):
    review["book_id"] = int(id)
    review["user_id"] = int(user)

    new_review = review_schema.load(review, session=db.session)
    db.session.add(new_review)
    db.session.commit()

    producer.send(KafkaTopic.REVIEW.value, key=KafkaKey.CREATE.value, value=review_schema.dump(new_review))

    return review_schema.dump(new_review), 201


def update(id, review, user):
    existing_review = Review.query.filter(Review.id == id).one_or_none()

    if not existing_review:
        abort(404, f"Review with id {id} not found.")

    if existing_review.user_id != int(user):
        abort(403, f"Review can only be edited by user who created it.")

    review["user_id"] = existing_review.user_id
    review["book_id"] = existing_review.book_id

    update_review = review_schema.load(review, session=db.session, instance=existing_review)
    db.session.merge(update_review)
    db.session.commit()

    producer.send(KafkaTopic.REVIEW.value, key=KafkaKey.UPDATE.value, value=review_schema.dump(update_review))

    return review_schema.dump(existing_review), 200


def delete(id, user):
    existing_review = Review.query.filter(Review.id == id).one_or_none()

    if not existing_review:
        abort(404, f"Review with id {id} not found.")

    if existing_review.user_id != int(user):
        abort(403, f"Review can only be deleted by user who created it.")

    db.session.delete(existing_review)
    db.session.commit()

    producer.send(KafkaTopic.REVIEW.value, key=KafkaKey.DELETE.value, value={"id": int(id)})

    return make_response(f"Review with id {id} successfully deleted.", 200)
