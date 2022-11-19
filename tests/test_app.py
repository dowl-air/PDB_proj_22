
from http import HTTPStatus

import pytest
from flask.testing import FlaskClient

from app.create_app import create_app, db, mongo

@pytest.fixture(scope='module', autouse=True)
def clear_db():
	with create_app().app_context():
		db.drop_all()
		mongo.connection['default'].drop_database('pdb')
	
@pytest.fixture
def client():
	with create_app().test_client() as client:
		yield client

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
