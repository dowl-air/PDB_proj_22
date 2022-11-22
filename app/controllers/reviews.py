from flask.helpers import make_response, abort

from entity.sql.base import db
from entity.sql.review import Review

from entity.sql.schemas import review_schema, reviews_schema


def get_all():
    reviews = Review.query.all()
    return reviews_schema.dump(reviews)


def get(id):
    review = Review.query.filter(Review.id == id).one_or_none()
    if review is not None:
        return review_schema.dump(review)
    else:
        abort(404, f"Review with id \"{id}\" not found.")


def create(review):
    new_review = review_schema.load(review, session=db.session)
    db.session.add(new_review)
    db.session.commit()
    return review_schema.dump(new_review), 201


def update(id, review):
    existing_review = Review.query.filter(Review.id == id).one_or_none()

    if existing_review:
        update_review = review_schema.load(review, session=db.session, instance=existing_review)
        db.session.merge(update_review)
        db.session.commit()
        return review_schema.dump(existing_review), 201
    else:
        abort(404, f"Review with id \"{id}\" not found.")


def delete(id):
    existing_review = Review.query.filter(Review.id == id).one_or_none()

    if existing_review:
        db.session.delete(existing_review)
        db.session.commit()
        return make_response(f"Review with id \"{id}\" successfully deleted.", 200)
    else:
        abort(404, f"Review with id \"{id}\" not found.")
