
from flask.testing import FlaskClient

from datetime import date
from http import HTTPStatus
from json import loads

from helpers import (
	protected_post, protected_patch,
	assert_error_response,
	find_by_id,
	format_date
)
from conftest import (
	RESERVATION_STATE_ACTIVE, RESERVATION_STATE_CLOSED,
	bc1984Brno1, bc1984Brno2, bcAnimalFarmBrno,
	userCustomerCustomer,
	reservationBrno
)

class TestReservation:
	new_id: int = 0

	def test_reservation_add(self, client: FlaskClient):
		USER = userCustomerCustomer

		BOOK_COPY = bc1984Brno2

		data = {
			'book_copy_id': BOOK_COPY.id
		}

		resp = protected_post('/reservations', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/profile/%d/reservations' % USER.id)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		reservation = find_by_id(self.new_id, json_data)
		assert reservation is not None
		assert reservation['book_copy_id'] == BOOK_COPY.id
		assert reservation['start_date'] == format_date(date.today())
		assert reservation['state'] == RESERVATION_STATE_ACTIVE

	def test_reservation_add_invalid_reserved(self, client: FlaskClient):
		USER = userCustomerCustomer

		BOOK_COPY = bcAnimalFarmBrno

		data = {
			'book_copy_id': BOOK_COPY.id
		}

		resp = protected_post('/reservations', data, client, USER)
		assert_error_response(resp)

	def test_reservation_add_invalid_borrowed(self, client: FlaskClient):
		USER = userCustomerCustomer

		BOOK_COPY = bc1984Brno1

		data = {
			'book_copy_id': BOOK_COPY.id
		}

		resp = protected_post('/reservations', data, client, USER)
		assert_error_response(resp)

	def test_reservation_cancel(self, client: FlaskClient):
		USER = userCustomerCustomer

		resp = protected_patch('/reservations/%d/cancel' % self.new_id, {}, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/profile/%d/reservations' % USER.id)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		reservation = find_by_id(self.new_id, json_data)
		assert reservation is not None
		assert reservation['state'] == RESERVATION_STATE_CLOSED

	def test_reservation_cancel_invalid(self, client: FlaskClient):
		USER = userCustomerCustomer

		# reservation is already closed
		resp = protected_patch('/reservations/%d/cancel' % reservationBrno.id, {}, client, USER)
		assert_error_response(resp)
