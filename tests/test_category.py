
from http import HTTPStatus
from json import loads

from helpers import (
	ClientWrapper,
	assert_error_response,
	find_by_id
)
from data import (
	book_Animal_Farm,
	category_fable,
	user_employee_Brno
)

class TestCategory:
	new_id: int = 0

	def test_category_add(self, client: ClientWrapper):
		USER = user_employee_Brno

		data = {
			'name': 'Novel',
			'description': 'A novel is a relatively long work of narrative fiction, typically...'
		}

		resp = client.protected_post('/categories', data, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/categories/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		category = loads(resp.data.decode())
		assert category['name'] == data['name']
		assert category['description'] == data['description']

	def test_category_add_invalid(self, client: ClientWrapper):
		USER = user_employee_Brno

		data = {
			'name': None,
			'description': 'Missing category name'
		}

		resp = client.protected_post('/categories', data, USER)
		assert_error_response(resp)

	def test_category_edit(self, client: ClientWrapper):
		USER = user_employee_Brno

		data = {
			'name': 'Edited category name',
			'description': 'Edited category description'
		}

		resp = client.protected_put('/categories/%d' % self.new_id, data, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/categories/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		category = loads(resp.data.decode())
		assert category['name'] == data['name']
		assert category['description'] == data['description']

	def test_category_edit_invalid(self, client: ClientWrapper):
		USER = user_employee_Brno

		data = {
			'name': None,
			'description': 'Invalid edit - no name'
		}

		resp = client.protected_put('/categories/%d' % self.new_id, data, USER)
		assert_error_response(resp)

	def test_category_edit_propagation(self, client: ClientWrapper):
		USER = user_employee_Brno

		CATEGORY = category_fable
		BOOK = book_Animal_Farm

		data = {
			'name': 'Fairy tale',
			'description': 'Fantastical story'
		}

		resp = client.protected_put('/categories/%d' % CATEGORY.id, data, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/books/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		category = find_by_id(CATEGORY.id, book['categories'])
		assert category is not None
		assert category['name'] == data['name']
		assert category['description'] == data['description']

	def test_category_delete(self, client: ClientWrapper):
		USER = user_employee_Brno

		resp = client.protected_delete('/categories/%d' % self.new_id, {}, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/categories/%d' % self.new_id)
		assert_error_response(resp)

	def test_category_delete_propagation(self, client: ClientWrapper):
		USER = user_employee_Brno

		CATEGORY = category_fable
		BOOK = book_Animal_Farm

		resp = client.get('/books/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		category = find_by_id(CATEGORY.id, book['categories'])
		assert category is not None

		resp = client.protected_delete('/categories/%d' % CATEGORY.id, {}, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/books/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		category = find_by_id(CATEGORY.id, book['categories'])
		assert category is None
