
from datetime import date
from http import HTTPStatus
from json import loads

from helpers import (
	ClientWrapper,
	assert_error_response, assert_ok_created,
	find_by_id,
	format_date
)
from data import (
	RESERVATION_STATE_ACTIVE, RESERVATION_STATE_CLOSED,
	bc_1984_Brno_1, bc_1984_Brno_2, bc_Animal_Farm_Brno,
	user_customer_Customer,
	reservation_Brno
)

class TestReservation:
	new_id: int = 0

	def test_reservation_add(self, client: ClientWrapper):
		client.login(user=user_customer_Customer)

		BOOK_COPY = bc_1984_Brno_2

		data = {
			'book_copy_id': BOOK_COPY.id
		}

		resp = client.post('/reservations', data)
		assert_ok_created(resp.status_code)
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		TestReservation.new_id = json_data['id']

		resp = client.get('/profile/reservations')
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		reservation = find_by_id(TestReservation.new_id, json_data)
		assert reservation is not None
		assert reservation['book_copy_id'] == BOOK_COPY.id
		assert reservation['start_date'] == format_date(date.today())
		assert reservation['state'] == RESERVATION_STATE_ACTIVE

	def test_reservation_add_invalid_reserved(self, client: ClientWrapper):
		client.login(user=user_customer_Customer)

		BOOK_COPY = bc_Animal_Farm_Brno

		data = {
			'book_copy_id': BOOK_COPY.id
		}

		resp = client.post('/reservations', data)
		assert_error_response(resp)

	def test_reservation_add_invalid_borrowed(self, client: ClientWrapper):
		client.login(user=user_customer_Customer)

		BOOK_COPY = bc_1984_Brno_1

		data = {
			'book_copy_id': BOOK_COPY.id
		}

		resp = client.post('/reservations', data)
		assert_error_response(resp)

	def test_reservation_cancel(self, client: ClientWrapper):
		client.login(user=user_customer_Customer)

		resp = client.patch('/reservations/%d/cancel' % TestReservation.new_id, {})
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/profile/reservations')
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		reservation = find_by_id(TestReservation.new_id, json_data)
		assert reservation is not None
		assert reservation['state'] == RESERVATION_STATE_CLOSED

	def test_reservation_cancel_invalid(self, client: ClientWrapper):
		client.login(user=user_customer_Customer)

		# reservation is already closed
		resp = client.patch('/reservations/%d/cancel' % reservation_Brno.id, {})
		assert_error_response(resp)
