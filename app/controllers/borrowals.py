from flask.helpers import make_response, abort
from datetime import date, timedelta

from entity import UserRole, BORROWAL_DAYS_LENGTH, BorrowalState, ReservationState, BookCopyState
from entity.sql.base import db
from entity.sql.borrowal import Borrowal
from entity.sql.reservation import Reservation
from entity.sql.book_copy import BookCopy
from entity.sql.user import User
from entity.sql.schemas import borrowal_schema, borrowals_schema

from controllers import producer
from apache_kafka.enums import KafkaKey, KafkaTopic


def get_active(user):
    employee_id = int(user)
    employee = User.query.filter(User.id == employee_id).one_or_none()
    if employee.role == UserRole.CUSTOMER.value:
        abort(403, f"You don't have rights to create borrowals.")

    bs = Borrowal.query.filter(Borrowal.state == BorrowalState.ACTIVE.value).all()
    return borrowals_schema.dump(bs), 200


def create(borrowal, user):
    employee_id = int(user)
    employee = User.query.filter(User.id == employee_id).one_or_none()
    if employee.role == UserRole.CUSTOMER.value:
        abort(403, f"You don't have rights to create borrowals.")

    customer_id = borrowal.get("customer_id")
    customer = User.query.filter(User.id == int(customer_id)).one_or_none()
    if not customer:
        abort(404, f"Customer with id {customer_id} doesn't exist.")

    # check if the book is not already borrowed
    old_borrowals = Borrowal.query.filter(Borrowal.book_copy_id == int(borrowal["book_copy_id"])).all()
    for b in old_borrowals:
        if (b.state == BorrowalState.ACTIVE.value):
            abort(409, "This book copy is already borrowed.")

    # check if the book is not deleted
    book_copy = BookCopy.query.filter(BookCopy.id == int(borrowal["book_copy_id"])).one_or_none()
    if book_copy.state == BookCopyState.DELETED.value:
        abort(404, "This book copy has been deleted.")

    # check if the book is not reserved
    reservations = Reservation.query.filter(Reservation.book_copy_id == int(borrowal["book_copy_id"])).all()
    for r in reservations:
        if (r.state == ReservationState.ACTIVE.value and r.end_date > date.today() and r.customer_id != customer_id):
            abort(409, "This book copy is already reserved by different customer.")
        if (r.customer_id == customer_id and r.state == ReservationState.ACTIVE.value):
            # mark reservation to be closed
            producer.send(KafkaTopic.RESERVATION.value, key=KafkaKey.DELETE.value, value={"id": r.id})
            db.session.delete(r)

    start_date = date.today()
    end_date = start_date + timedelta(days=BORROWAL_DAYS_LENGTH)
    borrowal["start_date"] = str(start_date)
    borrowal["end_date"] = str(end_date)

    borrowal["state"] = BorrowalState.ACTIVE.value

    new_borrowal = borrowal_schema.load(borrowal, session=db.session)
    db.session.add(new_borrowal)
    db.session.commit()

    borrowal_to_send = borrowal_schema.dump(new_borrowal)
    borrowal_to_send["employee_id"] = employee_id

    producer.send(KafkaTopic.BORROWAL.value, key=KafkaKey.CREATE.value, value=borrowal_to_send)

    return borrowal_schema.dump(new_borrowal), 201


def update(id, user):
    employee_id = int(user)
    employee = User.query.filter(User.id == employee_id).one_or_none()
    if employee.role == UserRole.CUSTOMER.value:
        abort(403, f"You don't have rights to return borrowed books.")

    existing_borrowal = Borrowal.query.filter(Borrowal.id == id).one_or_none()
    if not existing_borrowal:
        abort(404, f"Borrowal with id {id} not found.")

    if existing_borrowal.state != BorrowalState.ACTIVE.value:
        abort(404, f"Borrowal with id {id} already ended or has been lost.")

    existing_borrowal.state = BorrowalState.RETURNED.value
    db.session.add(existing_borrowal)
    db.session.commit()

    producer.send(KafkaTopic.BORROWAL.value, key=KafkaKey.DELETE.value, value={"id": int(id)})

    return borrowal_schema.dump(existing_borrowal), 200
