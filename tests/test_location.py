
from flask.testing import FlaskClient

from http import HTTPStatus
from json import loads

from helpers import (
	protected_post, protected_put, protected_delete,
	assert_error_response
)
from data import (
	location_Brno,
	bc_1984_Brno_1,
	user_admin_Admin
)

class TestLocation:
	new_id: int = 0

	def test_location_add(self, client: FlaskClient):
		USER = user_admin_Admin

		data = {
			'name': 'VUT FIT',
			'address': 'Božetěchova 1/2, 612 00 Brno-Královo Pole'
		}

		resp = protected_post('/locations', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/locations/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		location = loads(resp.data.decode())
		assert data['name'] == location['name']
		assert data['address'] == location['address']

	def test_location_add_invalid(self, client: FlaskClient):
		USER = user_admin_Admin

		data = {
			'address': 'Missing location name'
		}

		resp = protected_post('/locations', data, client, USER)
		assert_error_response(resp)

	def test_location_edit(self, client: FlaskClient):
		USER = user_admin_Admin

		data = {
			'name': 'Edited VUT FIT location',
			'address': 'Edited location address'
		}

		resp = protected_put('/locations/%d' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/locations/%d' % id)
		assert resp.status_code == HTTPStatus.OK
		location = loads(resp.data.decode())
		assert data['name'] == location['name']
		assert data['address'] == location['address']

	def test_location_edit_invalid(self, client: FlaskClient):
		USER = user_admin_Admin

		data = {
			'name': None,
			'description': 'Invalid edit - no name'
		}

		resp = protected_put('/locations/%d' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_location_edit_propagation(self, client: FlaskClient):
		USER = user_admin_Admin

		data = {
			'name': 'Ostrava',
			'address': 'idk'
		}

		LOCATION = location_Brno
		BOOK_COPY = bc_1984_Brno_1

		resp = protected_put('/locations/%d' % LOCATION.id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book-copies/%d' % BOOK_COPY.id)
		assert resp.status_code == HTTPStatus.OK
		book_copy = loads(resp.data.decode())
		assert book_copy['location']['name'] == data['name']
		assert book_copy['location']['address'] == data['address']

	def test_location_delete(self, client: FlaskClient):
		USER = user_admin_Admin

		resp = protected_delete('/locations/%d' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/locations/%d' % self.new_id)
		assert_error_response(resp)

	# cannot delete location with assigned book copies
	def test_location_delete_invalid(self, client: FlaskClient):
		USER = user_admin_Admin

		LOCATION = location_Brno

		resp = protected_delete('/locations/%d' % LOCATION.id, client, USER)
		assert_error_response(resp)
