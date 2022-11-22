
from flask.testing import FlaskClient

from http import HTTPStatus
from json import loads

from helpers import (
	protected_post, protected_put, protected_delete,
	assert_error_response,
	find_by_id
)
from conftest import (
	bookAnimalFarm,
	categoryFable,
	userEmployeeBrno
)

class TestCategory:
	new_id: int = 0

	def test_category_add(self, client: FlaskClient):
		USER = userEmployeeBrno

		data = {
			'name': 'Novel',
			'description': 'A novel is a relatively long work of narrative fiction, typically...'
		}

		resp = protected_post('/categories', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/categories/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		category = loads(resp.data.decode())
		assert category['name'] == data['name']
		assert category['description'] == data['description']

	def test_category_add_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno

		data = {
			'name': None,
			'description': 'Missing category name'
		}

		resp = protected_post('/categories', data, client, USER)
		assert_error_response(resp)

	def test_category_edit(self, client: FlaskClient):
		USER = userEmployeeBrno

		data = {
			'name': 'Edited category name',
			'description': 'Edited category description'
		}

		resp = protected_put('/categories/%d' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/categories/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		category = loads(resp.data.decode())
		assert category['name'] == data['name']
		assert category['description'] == data['description']

	def test_category_edit_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno

		data = {
			'name': None,
			'description': 'Invalid edit - no name'
		}

		resp = protected_put('/categories/%d' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_category_edit_propagation(self, client: FlaskClient):
		USER = userEmployeeBrno

		CATEGORY = categoryFable
		BOOK = bookAnimalFarm

		data = {
			'name': 'Fairy tale',
			'description': 'Fantastical story'
		}

		resp = protected_put('/categories/%d' % CATEGORY.id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/books/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		category = find_by_id(CATEGORY.id, book['categories'])
		assert category is not None
		assert category['name'] == data['name']
		assert category['description'] == data['description']

	def test_category_delete(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_delete('/categories/%d' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/categories/%d' % self.new_id)
		assert_error_response(resp)

	def test_category_delete_propagation(self, client: FlaskClient):
		USER = userEmployeeBrno

		CATEGORY = categoryFable
		BOOK = bookAnimalFarm

		resp = client.get('/books/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		category = find_by_id(CATEGORY.id, book['categories'])
		assert category is not None

		resp = protected_delete('/categories/%d' % CATEGORY.id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/books/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		category = find_by_id(CATEGORY.id, book['categories'])
		assert category is None
