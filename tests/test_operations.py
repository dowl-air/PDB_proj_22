
from flask.testing import FlaskClient

from datetime import date
from http import HTTPStatus
from json import loads

from helpers import login, expect_error, entity_compare, assert_dict_equal
from conftest import (
	embed_author_list,
	authorOrwell, authorHuxley, authorTolkien,
	book1984, bookBraveNewWorld, bookAnimalFarm,
	locationBrno,
	categoryFable
)
class TestCategory:
	new_category_id: int

	def test_category_add(self, client: FlaskClient):
		data = {
			'name': 'Novel',
			'description': 'A novel is a relatively long work of narrative fiction, typically...'
		}

		resp = client.post('/category/add', data=data)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_category_id = json_data['id']

		resp = client.get('/category/%d' % self.new_category_id)
		assert resp.status_code == HTTPStatus.OK
		category = loads(resp.data.decode())
		assert data['name'] == category['name']
		assert data['description'] == category['description']

	def test_category_add_invalid(self, client: FlaskClient):
		data = {
			'description': 'dsahbdsaansdana'
		}

		resp = client.post('/category/add', data=data)
		expect_error(resp)

	def test_category_edit(self, client: FlaskClient):
		data = {
			'name': 'Edited category',
			'description': 'Edited category description'
		}

		resp = client.patch('/category/%d/edit' % self.new_category_id, data=data)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/category/%d' % id)
		assert resp.status_code == HTTPStatus.OK
		category = loads(resp.data.decode())
		assert data['name'] == category['name']
		assert data['description'] == category['description']

	def test_category_edit_invalid(self, client: FlaskClient):
		data = {
			'name': None,
			'description': 'New description'
		}

		resp = client.patch('/category/add', data=data)
		expect_error(resp)

	def test_category_edit_propagation(self, client: FlaskClient):
		data = {
			'name': 'Fairy tale',
			'description': 'Fantastical story'
		}

		resp = client.patch('/category/%d/edit' % categoryFable, data=data)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % self.new_category_id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		assert_dict_equal(book['categories'], [data])
	
	def test_category_delete(self, client: FlaskClient):
		resp = client.delete('/category/%d/delete' % self.new_category_id)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/category/%d' % self.new_category_id)
		expect_error(resp)

	def test_category_delete_propagation(self, client: FlaskClient):
		resp = client.delete('/category/%d/delete' % categoryFable.id)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % bookAnimalFarm.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		assert len(book['categories']) == 1
		assert book['categories'][0]['id'] != categoryFable.id

NEW_USER_EMAIL = 'new_email@email.cz'

def test_register(client: FlaskClient):
	data = {
		'first_name': 'First',
		'last_name': 'Last',
		'email': NEW_USER_EMAIL,
		'password': 'password123'
	}

	resp = client.post('/register', data=data)
	assert resp.status_code == HTTPStatus.OK

	login(client, email=data['email'], password=data['password'])

def test_register_invalid(client: FlaskClient):
	data = {
		'first_name': 'X',
		'password': '123password'
	}

	resp = client.post('/register', data=data)
	expect_error(resp)

def test_register_duplicate_email(client: FlaskClient):
	data = {
		'first_name': 'Different',
		'last_name': 'Name',
		'email': NEW_USER_EMAIL,
		'password': 'abcdefg123'
	}

	resp = client.post('/register', data=data)
	expect_error(resp)

HOMAGE_TO_CATALONIA_DATA = {
	'name': 'Homage to Catalonia',
	'ISBN': '978-0-00-844274-3',
	'release_date': date(1938, 4, 25),
	'description': "In 1936 Orwell went to Spain to report on the Civil War...",
	'authors': [authorOrwell.id]
}

def test_add_book(client: FlaskClient):
	resp = client.post('/book/add', data=HOMAGE_TO_CATALONIA_DATA)
	assert resp.status_code == HTTPStatus.OK
	json_data = loads(resp.data.decode())
	assert 'id' in json_data

	HOMAGE_TO_CATALONIA_DATA['id'] = json_data['id']

	resp = client.get('/book/%d' % json_data['id'])
	assert resp.status_code == HTTPStatus.OK
	json_data = loads(resp.data.decode())
	assert json_data['name'] == HOMAGE_TO_CATALONIA_DATA['name']

	resp = client.get('/author/%d' % authorOrwell.id)
	assert resp.status_code == HTTPStatus.OK
	author = loads(resp.data.decode())
	assert len(author['books']) == 3
	assert len(filter(lambda x: x == HOMAGE_TO_CATALONIA_DATA['name'], author['books'])) == 1

def test_add_book_invalid(client: FlaskClient):
	data = {
		'release_date': date(1950, 11, 11),
		'description': 'text'
	}

	resp = client.post('/book/add', data=data)
	expect_error(resp)

def test_add_book_invalid_unknown_author(client: FlaskClient):
	data = {
		'name': 'The Stranger',
		'ISBN': '978-0679720201',
		'release_date': date(1942, 1, 1),
		'description': "In 1936 Orwell went to Spain to report on the Civil War...",
		'authors': [300]
	}

	resp = client.post('/book/add', data=data)
	expect_error(resp)

def test_update_book(client: FlaskClient):
	NEW_NAME = 'New name'
	NEW_DESCRIPTION = 'New description'
	NEW_AUTHORS = [authorHuxley.id, authorTolkien.id]
	data = {
		'id': book1984.id,
		'name': NEW_NAME,
		'ISBN': book1984.ISBN,
		'release_date': book1984.release_date,
		'description': NEW_DESCRIPTION,
		'authors': NEW_AUTHORS
	}

	resp = client.post('/book/%d/edit' % book1984.id, data=data)
	assert resp.status_code == HTTPStatus.OK

	edited_book = book1984
	edited_book.name = NEW_NAME
	edited_book.description = NEW_DESCRIPTION
	edited_book.authors = embed_author_list([authorHuxley, authorTolkien])

	resp = client.get('/book/%d' % book1984.id)
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, edited_book)

	resp = client.get('/author/%d' % authorHuxley.id)
	assert resp.status_code == HTTPStatus.OK
	author = loads(resp.data.decode())
	assert len(author['books']) == 2
	assert len(filter(lambda x: x == NEW_NAME, author['books'])) == 1

	book1984.save() # TODO

def test_delete_book(client: FlaskClient):
	resp = client.get('/book/%d' % HOMAGE_TO_CATALONIA_DATA['id'])
	assert resp.status_code == HTTPStatus.OK

	resp = client.delete('/book/%d/delete' % HOMAGE_TO_CATALONIA_DATA['id'])
	assert resp.status_code == HTTPStatus.OK

	resp = client.get('/book/%d')
	expect_error(resp)

	resp = client.get('/author/%d' % authorOrwell.id)
	assert resp.status_code == HTTPStatus.OK
	author = loads(resp.data.decode())
	assert len(author['books']) == 2
	assert len(filter(lambda x: x == HOMAGE_TO_CATALONIA_DATA['name'], author['books'])) == 0

def test_delete_book_invalid_existing_copies(client: FlaskClient):
	resp = client.delete('/book/%d/delete' % bookBraveNewWorld.id)
	expect_error(resp)

def test_add_book_copy(client: FlaskClient):
	data = {
		'book_id': book1984.id,
		'location_id': locationBrno.id,
		'print_date': date(2021, 10, 10),
		'note': 'Newly added'
	}

	resp = client.post('/book_copy/add')
	assert resp.status_code == HTTPStatus.OK
	json_data = loads(resp.data.decode())
	assert 'id' in json_data

	HOMAGE_TO_CATALONIA_DATA['id'] = json_data['id']

	resp = client.get('/author/%d' % authorOrwell.id)
	assert resp.status_code == HTTPStatus.OK
	author = loads(resp.data.decode())
	assert len(author['books']) == 3
	assert len(filter(lambda x: x == HOMAGE_TO_CATALONIA_DATA['name'], author['books'])) == 1
