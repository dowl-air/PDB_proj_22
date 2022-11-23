
from http import HTTPStatus
from json import loads

from helpers import (
	ClientWrapper,
	assert_error_response
)
from data import (
	location_Brno,
	bc_1984_Brno_1,
	user_admin_Admin
)

class TestLocation:
	new_id: int = 0

	def test_location_add(self, client: ClientWrapper):
		USER = user_admin_Admin

		data = {
			'name': 'VUT FIT',
			'address': 'Božetěchova 1/2, 612 00 Brno-Královo Pole'
		}

		resp = client.protected_post('/locations', data, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/locations/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		location = loads(resp.data.decode())
		assert data['name'] == location['name']
		assert data['address'] == location['address']

	def test_location_add_invalid(self, client: ClientWrapper):
		USER = user_admin_Admin

		data = {
			'address': 'Missing location name'
		}

		resp = client.protected_post('/locations', data, USER)
		assert_error_response(resp)

	def test_location_edit(self, client: ClientWrapper):
		USER = user_admin_Admin

		data = {
			'name': 'Edited VUT FIT location',
			'address': 'Edited location address'
		}

		resp = client.protected_put('/locations/%d' % self.new_id, data, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/locations/%d' % id)
		assert resp.status_code == HTTPStatus.OK
		location = loads(resp.data.decode())
		assert data['name'] == location['name']
		assert data['address'] == location['address']

	def test_location_edit_invalid(self, client: ClientWrapper):
		USER = user_admin_Admin

		data = {
			'name': None,
			'description': 'Invalid edit - no name'
		}

		resp = client.protected_put('/locations/%d' % self.new_id, data, USER)
		assert_error_response(resp)

	def test_location_edit_propagation(self, client: ClientWrapper):
		USER = user_admin_Admin

		data = {
			'name': 'Ostrava',
			'address': 'idk'
		}

		LOCATION = location_Brno
		BOOK_COPY = bc_1984_Brno_1

		resp = client.protected_put('/locations/%d' % LOCATION.id, data, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book-copies/%d' % BOOK_COPY.id)
		assert resp.status_code == HTTPStatus.OK
		book_copy = loads(resp.data.decode())
		assert book_copy['location']['name'] == data['name']
		assert book_copy['location']['address'] == data['address']

	def test_location_delete(self, client: ClientWrapper):
		USER = user_admin_Admin

		resp = client.protected_delete('/locations/%d' % self.new_id, {}, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/locations/%d' % self.new_id)
		assert_error_response(resp)

	# cannot delete location with assigned book copies
	def test_location_delete_invalid(self, client: ClientWrapper):
		USER = user_admin_Admin

		LOCATION = location_Brno

		resp = client.protected_delete('/locations/%d' % LOCATION.id, {}, USER)
		assert_error_response(resp)
