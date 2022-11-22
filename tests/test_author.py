
from flask.testing import FlaskClient

from http import HTTPStatus
from json import loads

from helpers import (
	assert_error_response,
	protected_post, protected_put, protected_delete
)
from conftest import (
	authorHuxley,
	bookBraveNewWorld,
	userEmployeeBrno
)

class TestAuthor:
	new_id: int

	def test_author_add(self, client: FlaskClient):
		data = {
			'first_name': 'Karel',
			'last_name': 'Čapek',
			'description': 'A czech 20th century novellist...'
		}

		USER = userEmployeeBrno

		resp = protected_post('/author/add', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/author/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		author = loads(resp.data.decode())
		assert data['first_name'] == author['first_name']
		assert data['last_name'] == author['last_name']
		assert data['description'] == author['description']

	def test_author_add_invalid(self, client: FlaskClient):
		data = {
			'first_name': 'Name',
			'description': 'Missing last name'
		}

		USER = userEmployeeBrno

		resp = protected_post('/author/add', data, client, USER)
		assert_error_response(resp)

	def test_author_edit(self, client: FlaskClient):
		data = {
			'first_name': 'Edited author first name',
			'last_name': 'Edited author last name',
			'description': 'Edited author description'
		}

		USER = userEmployeeBrno

		resp = protected_put('/author/%d/edit' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/author/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		author = loads(resp.data.decode())
		assert data['first_name'] == author['first_name']
		assert data['last_name'] == author['last_name']
		assert data['description'] == author['description']

	def test_author_edit_invalid(self, client: FlaskClient):
		data = {
			'first_name': None,
			'last_name': 'Last',
			'description': 'Invalid edit - no first name'
		}

		USER = userEmployeeBrno

		resp = protected_put('/author/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_author_edit_propagation(self, client: FlaskClient):
		data = {
			'first_name': 'Ray',
			'last_name': 'Bradbury',
			'description': 'Wrong author'
		}

		USER = userEmployeeBrno

		resp = protected_put('/author/%d/edit' % authorHuxley.id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % bookBraveNewWorld)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		assert len(book['authors']) == 1
		author = book['authors'][0]
		assert author['first_name'] == data['first_name']
		assert author['last_name'] == data['last_name']

	def test_author_delete(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_delete('/author/%d/delete' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/author/%d' % self.new_id)
		assert_error_response(resp)

	def test_author_delete_propagation(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_delete('/author/%d/delete' % authorHuxley.id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % bookBraveNewWorld.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		assert len(book['authors']) == 0
