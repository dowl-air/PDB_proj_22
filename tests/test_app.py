
from http import HTTPStatus

from flask.testing import FlaskClient

def test_hello_world(client: FlaskClient):
	resp = client.get('/')
	assert 'Hello, World!' == resp.data.decode()

def test_users(client: FlaskClient):
	resp = client.get('/users')
	assert 'Number of users: 0' == resp.data.decode()

def test_books(client: FlaskClient):
	resp = client.get('/books')
	assert "Book names: ['1984', 'Animal Farm', 'Brave New World', 'The Hobbit', 'Good Omens']" == resp.data.decode()

def test_add_book(client: FlaskClient):
	NEW_ID = 29
	resp = client.get('/add_book/%d' % NEW_ID)
	assert resp.status_code == HTTPStatus.OK

	resp = client.get('/books')
	assert "Book names: ['1984', 'Animal Farm', 'Brave New World', 'The Hobbit', 'Good Omens', '%s']" % NEW_ID == resp.data.decode()

def test_x(client: FlaskClient):
	json_book = '{"authors": [{"id": 1, "first_name": "George", "last_name": "Orwell"}], "_id": 1, "name": "1984", "ISBN": "978-80-7309-808-7", "release_date": {"$date": -648950400000}, "book_copies": [{"id": 1, "book_id": 1, "print_date": {"$date": 1412985600000}, "note": "Slightly used", "state": 1, "location_id": 1}, {"id": 2, "book_id": 1, "print_date": {"$date": 1642291200000}, "state": 3, "location_id": 1}, {"id": 3, "book_id": 1, "print_date": {"$date": 1610755200000}, "state": 1, "location_id": 2}, {"id": 4, "book_id": 1, "print_date": {"$date": 643248000000}, "state": 2, "location_id": 2}, {"id": 5, "book_id": 1, "print_date": {"$date": 1109030400000}, "note": "Lost", "state": 0, "location_id": 2}], "categories": [{"id": 1, "name": "Science-fiction"}, {"id": 2, "name": "Dystopia"}]}'
	from conftest import book1984
	from json import loads

	assert loads(json_book) == loads(book1984.to_json())