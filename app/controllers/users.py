from flask.helpers import make_response, abort

from entity.sql.base import db
from entity.sql.user import User

from entity.sql.schemas import user_schema, users_schema


def create(user):
    email = user.get("email")
    existing_user = User.query.filter(User.email == email).one_or_none()

    if existing_user is None:
        new_user = user_schema.load(user, session=db.session)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user), 201
    else:
        abort(406, f"User with email {email} already exists.")
