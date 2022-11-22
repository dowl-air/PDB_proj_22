
from flask.testing import FlaskClient

from http import HTTPStatus
from json import loads

from helpers import (
	assert_error_response,
	protected_post, protected_put, protected_delete
)
from conftest import (
	locationBrno,
	bc1984Brno1,
	userAdmin
)

class TestLocation:
	new_id: int = 0

	def test_location_add(self, client: FlaskClient):
		data = {
			'name': 'VUT FIT',
			'address': 'Božetěchova 1/2, 612 00 Brno-Královo Pole'
		}

		USER = userAdmin

		resp = protected_post('/location/add', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/location/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		location = loads(resp.data.decode())
		assert data['name'] == location['name']
		assert data['address'] == location['address']

	def test_location_add_invalid(self, client: FlaskClient):
		data = {
			'address': 'Missing location name'
		}

		USER = userAdmin

		resp = protected_post('/location/add', data, client, USER)
		assert_error_response(resp)

	def test_location_edit(self, client: FlaskClient):
		data = {
			'name': 'Edited VUT FIT location',
			'address': 'Edited location address'
		}

		USER = userAdmin

		resp = protected_put('/location/%d/edit' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/location/%d' % id)
		assert resp.status_code == HTTPStatus.OK
		location = loads(resp.data.decode())
		assert data['name'] == location['name']
		assert data['address'] == location['address']

	def test_location_edit_invalid(self, client: FlaskClient):
		data = {
			'name': None,
			'description': 'Invalid edit - no name'
		}

		USER = userAdmin

		resp = protected_put('/location/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_location_edit_propagation(self, client: FlaskClient):
		data = {
			'name': 'Ostrava',
			'address': 'idk'
		}

		USER = userAdmin

		resp = protected_put('/location/%d/edit' % locationBrno.id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book_copy/%d' % bc1984Brno1.id)
		assert resp.status_code == HTTPStatus.OK
		book_copy = loads(resp.data.decode())
		assert book_copy['location']['name'] == data['name']
		assert book_copy['location']['address'] == data['address']

	def test_location_delete(self, client: FlaskClient):
		USER = userAdmin

		resp = protected_delete('/location/%d/delete' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/location/%d' % self.new_id)
		assert_error_response(resp)

	# cannot delete location with assigned book copies
	def test_location_delete_invalid(self, client: FlaskClient):
		USER = userAdmin

		resp = protected_delete('/location/%d/delete' % locationBrno.id, client, USER)
		assert_error_response(resp)
