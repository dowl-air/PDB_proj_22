
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from deepdiff.diff import DeepDiff

from datetime import date
from http import HTTPStatus
from json import loads, dumps

from typing import Optional

from app.entity.nosql import (
	Location, Category, Author, Book, BookCopy, User, Borrowal, Reservation, Review,
	EmbeddedCategory, EmbeddedBook, EmbeddedLocation, EmbeddedBookCopy, AuthorName, EmbeddedUser
)

# asserts that the response is an error
# (other than unauthorized access or default nonexistent endpoint)
def assert_error_response(resp: TestResponse) -> None:
	assert resp.status_code != HTTPStatus.OK
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

def assert_ok_created(status_code: int) -> None:
	assert status_code == HTTPStatus.OK or status_code == HTTPStatus.CREATED

def find(fn, arr: list):
	arr = list(filter(fn, arr))
	if arr != 1:
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
	def __init__(self, client: FlaskClient) -> None:
		self.client = client
		self.token: Optional[str] = None

	def set_token(self, token: Optional[str]) -> None:
		self.token = token

	def get(self, endpoint: str, *, token: Optional[str] = None) -> TestResponse:
		return self.client.get(endpoint, headers=self._auth_headers(token))

	def post(self, endpoint: str, data: dict, *, token: Optional[str] = None) -> TestResponse:
		return self.client.post(endpoint, data=dumps(data), content_type='application/json', headers=self._auth_headers(token))

	def delete(self, endpoint: str, data: dict, *, token: Optional[str] = None) -> TestResponse:
		return self.client.delete(endpoint, data=dumps(data), content_type='application/json', headers=self._auth_headers(token))

	def put(self, endpoint: str, data: dict, *, token: Optional[str] = None) -> TestResponse:
		return self.client.put(endpoint, data=dumps(data), content_type='application/json', headers=self._auth_headers(token))

	def patch(self, endpoint: str, data: dict, *, token: Optional[str] = None) -> TestResponse:
		return self.client.patch(endpoint, data=dumps(data), content_type='application/json', headers=self._auth_headers(token))

	def login(self, user: User) -> None:
		data = {
			'email': user.email,
			'password': user.last_name.lower()
		}

		resp = self.post('/login', data)
		assert resp.status_code == HTTPStatus.OK
		self.set_token(resp.data.decode())

	def logout(self) -> None:
		resp = self.client.post('/logout', {})
		assert resp.status_code == HTTPStatus.OK
		self.token = None

	def _auth_headers(self, token: Optional[str]) -> Optional[dict]:
		if token is None:
			if self.token is None:
				return None
			token = self.token
		return {'Authorization': f'Bearer {token}'}

# converts a mongo entity to a dict (or a list of entities to a list of dicts)
def to_json(x) -> dict:
	if x is None:
		return None
	elif isinstance(x, list):
		return list(map(lambda x: to_json(x), x))
	elif isinstance(x, Location):
		return {
			'id': x.id,
			'name': x.name,
			'address': x.address
		}
	elif isinstance(x, Category):
		return {
			'id': x.id,
			'name': x.name,
			'description': x.description
		}
	elif isinstance(x, Author):
		return {
			'id': x.id,
			'first_name': x.first_name,
			'last_name': x.last_name,
			'description': x.description,
			'books': to_json(x.books)
		}
	elif isinstance(x, Book):
		return {
			'id': x.id,
			'authors': to_json(x.authors),
			'name': x.name,
			'ISBN': x.ISBN,
			'release_date': format_date(x.release_date),
			'description': x.description,
			'book_copies': to_json(x.book_copies),
			'categories': to_json(x.categories)
		}
	elif isinstance(x, BookCopy):
		return {
			'id': x.id,
			'book_id': x.book_id,
			'print_date': format_date(x.print_date),
			'note': x.note,
			'state': x.state,
			'location': to_json(x.location)
		}
	elif isinstance(x, User):
		return {
			'id': x.id,
			'first_name': x.first_name,
			'last_name': x.last_name,
			'role': x.role,
			'email': x.email
		}
	elif isinstance(x, Borrowal):
		return {
			'id': x.id,
			'start_date': format_date(x.start_date),
			'end_date': format_date(x.end_date),
			'returned_date': format_date(x.returned_date),
			'state': x.state,
			'book_copy': to_json(x.book_copy),
			'customer': to_json(x.customer),
			'employee': to_json(x.employee),
		}
	elif isinstance(x, Reservation):
		return {
			'id': x.id,
			'start_date': format_date(x.start_date),
			'end_date': format_date(x.end_date),
			'state': x.state,
			'book_copy': to_json(x.book_copy),
			'customer': to_json(x.customer)
		}
	elif isinstance(x, Review):
		return {
			'id': x.id,
			'book_id': x.book_id,
			'title': x.title,
			'content': x.content,
			'rating': x.rating,
			'customer': to_json(x.customer)
		}
	elif isinstance(x, AuthorName):
		return {
			'id': x.id,
			'first_name': x.first_name,
			'last_name': x.last_name
		},
	elif isinstance(x, EmbeddedLocation):
		return {
			'id': x.id,
			'name': x.name,
			'address': x.address
		}
	elif isinstance(x, EmbeddedCategory):
		return {
			'id': x.id,
			'name': x.name,
			'description': x.description
		}
	elif isinstance(x, EmbeddedBookCopy):
		return {
			'id': x.id,
			'book_id': x.book_id,
			'print_date': format_date(x.print_date),
			'note': x.note,
			'state': x.state,
			'location_id': x.location_id
		}
	elif isinstance(x, EmbeddedUser):
		return {
			'id': x.id,
			'first_name': x.first_name,
			'last_name': x.last_name,
			'role': x.role,
			'email': x.email
		}
	elif isinstance(x, EmbeddedBook):
		return {
			'id': x.id,
			'name': x.name,
			'ISBN': x.ISBN,
			'release_date': format_date(x.release_date),
			'description': x.description
		}
	else:
		raise Exception('to_json: Unexpected type')
