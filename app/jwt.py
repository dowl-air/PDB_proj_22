
import time
from http import HTTPStatus

from werkzeug.exceptions import Unauthorized
from flask.helpers import abort
from jose import JWTError, jwt

from entity.sql.user import User

JWT_ISSUER = 'pdb_project'
JWT_SECRET = 'hidden_secret'
JWT_LIFETIME_SECONDS = 600
JWT_ALGORITHM = 'HS256'


def generate_token(user: dict) -> str:
    email = user["email"]
    existing_user: User = User.query.filter(User.email == email).one_or_none()
    if not existing_user:
        abort(HTTPStatus.NOT_FOUND, f"User with email {email} not found.")

    password = user["password"]
    if password != existing_user.password:
        abort(HTTPStatus.UNAUTHORIZED, f"Wrong password for email {email}.")

    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(existing_user.id),
    }

    return jwt.encode(payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_token(token) -> dict:
    try:
        return jwt.decode(token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise Unauthorized() from e

def check_authorized(user: str, token_info: dict) -> str:
    return {
        'message': 'You are authorized.',
        'user_id': int(user),
        'token_info': token_info
    }

def _current_timestamp() -> int:
    return int(time.time())
