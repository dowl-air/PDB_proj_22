
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from deepdiff.diff import DeepDiff

from datetime import date
from http import HTTPStatus
from json import loads, dumps
from time import sleep

from typing import Optional, Union

from app.entity.nosql import (
    Location, Category, Author, Book, BookCopy, User, Borrowal, Reservation, Review,
    EmbeddedCategory, EmbeddedBook, EmbeddedLocation, EmbeddedBookCopy, AuthorName, EmbeddedUser
)


class InvalidTestException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)

# asserts that the response is an error
# (other than unauthorized access or default nonexistent endpoint)
def assert_error_response(resp: TestResponse) -> None:
    assert resp.status_code != HTTPStatus.OK
    assert resp.status_code != HTTPStatus.CREATED
    assert resp.status_code != HTTPStatus.UNAUTHORIZED
    assert resp.data.decode() is not None

    # check that this is not an automated response to a nonexistent endpoint
    if resp.status_code == HTTPStatus.NOT_FOUND:
        json_data = loads(resp.data.decode())
        assert json_data['detail'] != 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'

# asserts that JSON objects equal while ignoring additional fields in the tested object
def assert_dict_equal(actual, expected, ignore_list=['dictionary_item_removed', 'iterable_item_removed']) -> None:
    diff = DeepDiff(actual, expected, ignore_order=True, report_repetition=True)
    diff_keys = list(diff.keys())
    if diff_keys:
        diff_keys = list(filter(lambda x: x not in ignore_list, diff_keys))
        if len(diff_keys) == 0:
            return

    assert actual == expected

def find(fn, arr: list):
    arr = list(filter(fn, arr))
    if len(arr) != 1:
        return None
    return arr[0]

def find_by_id(id: int, arr: list):
    if len(arr) == 0 or not isinstance(arr[0], dict):
        return None
    return find(lambda x: x['id'] == id, arr)

def format_date(d: Optional[date]) -> Optional[str]:
    if d is None:
        return None
    return d.strftime('%Y-%m-%d')

# wrapper around a flask test client
class ClientWrapper:
    TYPE_GET = 'GET'
    TYPE_POST = 'POST'
    TYPE_DELETE = 'DELETE'
    TYPE_PUT = 'PUT'
    TYPE_PATCH = 'PATCH'

    OPERATION_REQUEST_TYPES = [TYPE_POST, TYPE_DELETE, TYPE_PUT, TYPE_PATCH]

    DEFAULT_OPERATION_DELAY: float = 2.0

    def __init__(self, client: FlaskClient) -> None:
        self.client = client
        self.token: Optional[str] = None

        self.delay: Optional[float] = ClientWrapper.DEFAULT_OPERATION_DELAY
        self.used_operation = False

    # how many seconds to wait after every request that is an operation
    # used to wait for operation to finish modifiying data in MongoDB
    def set_operation_delay(self, delay: Optional[float]) -> None:
        if delay > 0:
            self.delay = delay
        else:
            raise InvalidTestException('Delay must be a positive amount of seconds, set to None to disable')

    def set_token(self, token: Optional[str]) -> None:
        self.token = token

    def _send_request(self, reqtype: str, endpoint: str, data: Optional[dict] = None, token: Optional[str] = None) -> TestResponse:
        headers = self._auth_headers(token)
        CONTENT_TYPE = 'application/json'

        if reqtype in ClientWrapper.OPERATION_REQUEST_TYPES:
            self.used_operation = True
        else:
            # waits before every query that follows an operation
            if self.delay is not None and self.used_operation:
                sleep(self.delay)

            self.used_operation = False

        if reqtype == ClientWrapper.TYPE_GET:
            resp = self.client.get(endpoint, headers=headers)
        elif reqtype == ClientWrapper.TYPE_POST:
            resp = self.client.post(endpoint, data=dumps(data), content_type=CONTENT_TYPE, headers=headers)
        elif reqtype == ClientWrapper.TYPE_DELETE:
            resp = self.client.delete(endpoint, data=dumps(data), content_type=CONTENT_TYPE, headers=headers)
        elif reqtype == ClientWrapper.TYPE_PUT:
            resp = self.client.put(endpoint, data=dumps(data), content_type=CONTENT_TYPE, headers=headers)
        elif reqtype == ClientWrapper.TYPE_PATCH:
            resp = self.client.patch(endpoint, data=dumps(data), content_type=CONTENT_TYPE, headers=headers)
        else:
            raise InvalidTestException(f"Unsupported request type '{type}'")

        return resp

    def get(self, endpoint: str, *, token: Optional[str] = None) -> TestResponse:
        return self._send_request(ClientWrapper.TYPE_GET, endpoint, token=token)

    def post(self, endpoint: str, data: dict, *, token: Optional[str] = None) -> TestResponse:
        return self._send_request(ClientWrapper.TYPE_POST, endpoint, data, token)

    def delete(self, endpoint: str, data: dict, *, token: Optional[str] = None) -> TestResponse:
        return self._send_request(ClientWrapper.TYPE_DELETE, endpoint, data, token)

    def put(self, endpoint: str, data: dict, *, token: Optional[str] = None) -> TestResponse:
        return self._send_request(ClientWrapper.TYPE_PUT, endpoint, data, token)

    def patch(self, endpoint: str, data: dict, *, token: Optional[str] = None) -> TestResponse:
        return self._send_request(ClientWrapper.TYPE_PATCH, endpoint, data, token)

    def login(self, *, user: Optional[User] = None, email: Optional[str] = None, password: Optional[str] = None) -> None:
        if user is not None:
            data = {
                'email': user.email,
                'password': user.last_name.lower()
            }
        elif email is not None and password is not None:
            data = {
                'email': email,
                'password': password
            }
        else:
            raise InvalidTestException('Pass either a user object or an email and password')

        resp = self.post('/login', data)
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        self.set_token(json_data['token'])

    # simply throws away the token (simulates logout on frontend)
    def logout(self) -> None:
        self.token = None

    def _auth_headers(self, token: Optional[str]) -> Optional[dict]:
        if token is None:
            if self.token is None:
                return None
            token = self.token
        return {'Authorization': f'Bearer {token}'}

# converts a mongo entity to a dict (or a list of entities to a list of dicts)
def to_json(arg, no_none_values: bool = True) -> dict:
    res = _to_json(arg)
    if no_none_values:
        return delete_none_values(res)
    return res

def _to_json(arg) -> dict:
    if arg is None:
        return None
    elif isinstance(arg, list):
        return list(map(lambda x: _to_json(x), arg))
    elif isinstance(arg, Location):
        return {
            'id': arg.id,
            'name': arg.name,
            'address': arg.address
        }
    elif isinstance(arg, Category):
        return {
            'id': arg.id,
            'name': arg.name,
            'description': arg.description
        }
    elif isinstance(arg, Author):
        return {
            'id': arg.id,
            'first_name': arg.first_name,
            'last_name': arg.last_name,
            'description': arg.description,
            'books': _to_json(arg.books)
        }
    elif isinstance(arg, Book):
        return {
            'id': arg.id,
            'authors': _to_json(arg.authors),
            'name': arg.name,
            'ISBN': arg.ISBN,
            'release_date': format_date(arg.release_date),
            'description': arg.description,
            'book_copies': _to_json(arg.book_copies),
            'categories': _to_json(arg.categories)
        }
    elif isinstance(arg, BookCopy):
        return {
            'id': arg.id,
            'book_id': arg.book_id,
            'print_date': format_date(arg.print_date),
            'note': arg.note,
            'state': arg.state,
            'location': _to_json(arg.location)
        }
    elif isinstance(arg, User):
        return {
            'id': arg.id,
            'first_name': arg.first_name,
            'last_name': arg.last_name,
            'role': arg.role,
            'email': arg.email
        }
    elif isinstance(arg, Borrowal):
        return {
            'id': arg.id,
            'start_date': format_date(arg.start_date),
            'end_date': format_date(arg.end_date),
            'returned_date': format_date(arg.returned_date),
            'state': arg.state,
            'book_copy': _to_json(arg.book_copy),
            'customer': _to_json(arg.customer),
            'employee': _to_json(arg.employee),
        }
    elif isinstance(arg, Reservation):
        return {
            'id': arg.id,
            'start_date': format_date(arg.start_date),
            'end_date': format_date(arg.end_date),
            'state': arg.state,
            'book_copy': _to_json(arg.book_copy),
            'customer': _to_json(arg.customer)
        }
    elif isinstance(arg, Review):
        return {
            'id': arg.id,
            'book_id': arg.book_id,
            'title': arg.title,
            'content': arg.content,
            'rating': arg.rating,
            'customer': _to_json(arg.customer)
        }
    elif isinstance(arg, AuthorName):
        return {
            'id': arg.id,
            'first_name': arg.first_name,
            'last_name': arg.last_name
        }
    elif isinstance(arg, EmbeddedLocation):
        return {
            'id': arg.id,
            'name': arg.name,
            'address': arg.address
        }
    elif isinstance(arg, EmbeddedCategory):
        return {
            'id': arg.id,
            'name': arg.name,
            'description': arg.description
        }
    elif isinstance(arg, EmbeddedBookCopy):
        return {
            'id': arg.id,
            'book_id': arg.book_id,
            'print_date': format_date(arg.print_date),
            'note': arg.note,
            'state': arg.state,
            'location_id': arg.location_id
        }
    elif isinstance(arg, EmbeddedUser):
        return {
            'id': arg.id,
            'first_name': arg.first_name,
            'last_name': arg.last_name,
            'role': arg.role,
            'email': arg.email
        }
    elif isinstance(arg, EmbeddedBook):
        return {
            'id': arg.id,
            'name': arg.name,
            'ISBN': arg.ISBN,
            'release_date': format_date(arg.release_date),
            'description': arg.description
        }
    else:
        raise InvalidTestException('Unexpected type')

def delete_none_values(arg: Union[list, dict]) -> Union[list, dict]:
    if isinstance(arg, list):
        return list(map(lambda x: delete_none_values(x), arg))

    for key, val in list(arg.items()):
        if isinstance(val, dict):
            delete_none_values(val)
        elif isinstance(val, list):
            for it in val:
                if isinstance(it, dict) or isinstance(it, list):
                    delete_none_values(it)
        elif val is None:
            del arg[key]

    return arg
