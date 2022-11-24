from flask.helpers import make_response, abort

from entity.sql.base import db
from entity.sql.borrowal import Borrowal
from entity.sql.user import User

from entity.sql.schemas import borrowal_schema, borrowals_schema
from datetime import date


def create(borrowal):
    user_id = borrowal.get("customer_id")
    existing_user = User.query.filter(User.id == user_id).one_or_none()

    if existing_user is not None:
        if borrowal.get("start_date") is None:
            borrowal["start_date"] = str(date.today())
        new_borrowal = borrowal_schema.load(borrowal, session=db.session)
        db.session.add(new_borrowal)
        db.session.commit()
        return borrowal_schema.dump(new_borrowal), 201
    else:
        abort(404, f"User with id {user_id} doesn't exist.")


def update(id):
    # finish borrowal
    existing_borrowal = Borrowal.query.filter(Borrowal.id == id).one_or_none()
    if not existing_borrowal:
        abort(404, f"Borrowal with id \"{id}\" not found.")

    existing_borrowal.state = 1
    db.session.merge(existing_borrowal)
    db.session.commit()

    return borrowal_schema.dump(existing_borrowal), 201
