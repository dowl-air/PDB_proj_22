from flask.helpers import make_response, abort

from entity.sql.base import db
from entity.sql.user import User

from entity.nosql.review import Review
from entity.nosql.reservation import Reservation
from entity.nosql.borrowal import Borrowal

from entity.sql.schemas import user_schema, users_schema
from entity.nosql.schemas_mongo import reviews_schema, reservations_schema, borrowals_schema


def get(user):
    # Get user object of currently signed in user
    user_id = int(user)
    existing_user = User.query.filter(User.id == user_id).one_or_none()
    if not existing_user:
        abort(404, f"User with id {user_id} not found.")
    return user_schema.dump(existing_user), 200


def get_reviews(user):
    # get reviews of one specific user, who is signed in
    user_id = int(user)
    reviews = Review.objects(customer__id=user_id)
    return reviews_schema.dump(reviews), 200


def get_reservations(user):
    # get reservations of one specific user, who is signed in
    user_id = int(user)
    reservations = Reservation.objects(customer__id=user_id)
    return reservations_schema.dump(reservations), 200


def get_borrowals(user):
    # get reservations of one specific user, who is signed in
    user_id = int(user)
    borrowals = Borrowal.objects(customer__id=user_id)
    return borrowals_schema.dump(borrowals), 200


def create(user):
    # create new user
    email = user.get("email")
    existing_user = User.query.filter(User.email == email).one_or_none()

    if existing_user is None:
        new_user = user_schema.load(user, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201
    else:
        abort(406, f"User with email {email} already exists.")


def update(user, user_data):
    # Update currenty signed in user with user_data object
    user_id = int(user)
    existing_user = User.query.filter(User.id == user_id).one_or_none()

    if not existing_user:
        abort(404, f"User with id {user_id} not found.")
    if not "email" in user_data:
        user_data["email"] = existing_user.email
    if not "password" in user_data:
        user_data["password"] = existing_user.password
    update_user = user_schema.load(user_data, session=db.session, instance=existing_user)
    db.session.merge(update_user)
    db.session.commit()
    return user_schema.dump(update_user), 200
