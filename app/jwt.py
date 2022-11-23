import time

import connexion
import six
from werkzeug.exceptions import Unauthorized
from flask.helpers import abort
from jose import JWTError, jwt

from entity.sql.user import User

JWT_ISSUER = 'com.zalando.connexion'
JWT_SECRET = 'hidden_secret'
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'


def generate_token(user):
    email = user.get("email")
    existing_user = User.query.filter(User.email == email).one_or_none()
    if not existing_user:
        abort(404, f"User with email {email} not found.")

    password = user.get("password")
    if password != existing_user.password:
        abort(401, f"Wrong password for email {email}.")

    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(existing_user.id),
    }

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        six.raise_from(Unauthorized, e)


def check_authorized(user, token_info) -> str:
    return '''
    You are authorized. 
    user_id: {user}
    token: {token_info}
    '''.format(user=user, token_info=token_info)


def _current_timestamp() -> int:
    return int(time.time())
