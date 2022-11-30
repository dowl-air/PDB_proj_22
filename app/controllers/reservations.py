from datetime import date, timedelta

from flask.helpers import make_response, abort

from entity import ReservationState, RESERVATION_DAYS_LENGTH, BookCopyState, BorrowalState
from entity.sql.base import db
from entity.sql.reservation import Reservation
from entity.sql.borrowal import Borrowal
from entity.sql.book_copy import BookCopy
from entity.sql.user import User
from entity.sql.schemas import reservation_schema, reservations_schema

from controllers import producer
from apache_kafka.enums import KafkaKey, KafkaTopic


def create(reservation, user):
    customer_id = int(user)
    start_date = date.today()
    end_date = start_date + timedelta(days=RESERVATION_DAYS_LENGTH)

    # check if the book is not already borrowed
    old_borrowals = Borrowal.query.filter(Borrowal.book_copy_id == int(reservation["book_copy_id"])).all()
    for b in old_borrowals:
        if (b.state == BorrowalState.ACTIVE.value):
            abort(409, "This book copy is already borrowed.")

    # check if the book is not deleted
    book_copy = BookCopy.query.filter(BookCopy.id == int(reservation["book_copy_id"])).one_or_none()
    if book_copy.state == BookCopyState.DELETED.value:
        abort(404, "This book copy has been deleted.")

    # check if the book is not reserved
    reservations = Reservation.query.filter(Reservation.book_copy_id == int(reservation["book_copy_id"])).all()
    for r in reservations:
        if (r.state == ReservationState.ACTIVE.value and r.end_date > date.today()):
            abort(409, "This book copy is already reserved.")
        if (r.customer_id == customer_id and r.state == ReservationState.ACTIVE.value):
            # mark reservation to be closed
            producer.send(KafkaTopic.RESERVATION.value, key=KafkaKey.DELETE.value, value={"id": r.id})
            db.session.delete(r)

    reservation["customer_id"] = customer_id
    reservation["start_date"] = str(start_date)
    reservation["end_date"] = str(end_date)
    reservation["state"] = ReservationState.ACTIVE.value

    new_reservation = reservation_schema.load(reservation, session=db.session)
    db.session.add(new_reservation)
    db.session.commit()

    producer.send(KafkaTopic.RESERVATION.value, key=KafkaKey.CREATE.value, value=reservation_schema.dump(new_reservation))

    return reservation_schema.dump(new_reservation), 201


def delete(id, user):
    existing_reservation = Reservation.query.filter(Reservation.id == id).one_or_none()
    if not existing_reservation:
        abort(404, f"Reservation with id {id} not found.")

    if int(existing_reservation.state) == ReservationState.CLOSED.value:
        abort(409, f"Reservation with id {id} is already canceled.")

    if int(user) != int(existing_reservation.customer_id):
        abort(409, f"Reservation needs to be deleted by the user who created them.")

    # we dont need deleted reservations in SQL
    db.session.delete(existing_reservation)
    db.session.commit()

    # will be stored in mongo with state changed
    producer.send(KafkaTopic.RESERVATION.value, key=KafkaKey.DELETE.value, value={"id": int(id)})

    return make_response(f"Reservation with id {id} successfully deleted.", 200)
