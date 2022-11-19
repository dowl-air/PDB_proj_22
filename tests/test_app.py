
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
	assert 'Book names: []' == resp.data.decode()

def test_add_book(client: FlaskClient):
	NEW_ID = 29
	resp = client.get('/add_book/%d' % NEW_ID)
	assert resp.status_code == HTTPStatus.OK

	resp = client.get('/books')
	assert "Book names: ['%s']" % NEW_ID == resp.data.decode()
