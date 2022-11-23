from flask.helpers import make_response, abort

from entity.sql.base import db
from entity.sql.reservation import Reservation
from entity.sql.user import User

from entity.sql.schemas import reservation_schema, reservations_schema


def create(reservation):
    user_id = reservation.get("customer_id")
    existing_user = User.query.filter(User.id == user_id).one_or_none()

    if existing_user is not None:
        new_reservation = reservation_schema.load(reservation, session=db.session)
        db.session.add(new_reservation)
        db.session.commit()
        return reservation_schema.dump(new_reservation), 201
    else:
        abort(404, f"User with id {user_id} doesn't exist.")


def delete(id):
    existing_reservation = Reservation.query.filter(Reservation.id == id).one_or_none()
    if not existing_reservation:
        abort(404, f"Reservation with id \"{id}\" not found.")

    """  existing_user = User.query.filter(User.id == user.user_id).one_or_none()
    if not existing_user:
        abort(404, f"Reservation needs to be deleted by the user who created them. User with id \"{id}\" not found.")

    if existing_user.id != user.user_id:
        abort(404, f"Reservation needs to be deleted by the user who created them.")
    """
    db.session.delete(existing_reservation)
    db.session.commit()
    return make_response(f"Reservation with id \"{id}\" successfully deleted.", 200)
