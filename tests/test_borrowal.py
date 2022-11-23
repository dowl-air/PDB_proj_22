
from datetime import date
from http import HTTPStatus
from json import loads

from helpers import (
	ClientWrapper,
	assert_error_response,
	find_by_id,
	format_date
)
from data import (
	BORROWAL_STATE_ACTIVE, BORROWAL_STATE_RETURNED,
	bc_1984_Brno_1, bc_Animal_Farm_Brno, bc_Hobbit_Olomouc,
	user_employee_Brno, user_customer_Customer,
	borrowal_London_3
)

class TestBorrowal:
	new_id: int = 0

	def test_borrowal_add(self, client: ClientWrapper):
		client.login(user_employee_Brno)

		BOOK_COPY = bc_Hobbit_Olomouc
		CUSTOMER = user_customer_Customer

		data = {
			'book_copy_id': BOOK_COPY.id,
			'customer_id': CUSTOMER.id
		}

		resp = client.post('/borrowals', data)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		client.logout()
		client.login(CUSTOMER)

		resp = client.get('/profile/borrowals')
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		borrowal = find_by_id(self.new_id, json_data)
		assert borrowal['book_copy_id'] == BOOK_COPY.id
		assert borrowal['start_date'] == format_date(date.today())
		assert borrowal['state'] == BORROWAL_STATE_ACTIVE

	def test_borrowal_add_invalid_reserved(self, client: ClientWrapper):
		client.login(user_employee_Brno)

		BOOK_COPY = bc_Animal_Farm_Brno
		CUSTOMER = user_customer_Customer

		data = {
			'book_copy_id': BOOK_COPY.id,
			'customer_id': CUSTOMER.id
		}

		resp = client.post('/borrowals', data)
		assert_error_response(resp)

	def test_borrowal_add_invalid_borrowed(self, client: ClientWrapper):
		client.login(user_employee_Brno)

		BOOK_COPY = bc_1984_Brno_1
		CUSTOMER = user_customer_Customer

		data = {
			'book_copy_id': BOOK_COPY.id,
			'customer_id': CUSTOMER.id
		}

		resp = client.post('/borrowals', data)
		assert_error_response(resp)

	def test_borrowal_return(self, client: ClientWrapper):
		client.login(user_employee_Brno)

		resp = client.patch('/borrowals/%d/return' % self.new_id, {})
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/active_borrowals')
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		borrowal = find_by_id(self.new_id, json_data)
		assert borrowal is not None
		assert borrowal['state'] == BORROWAL_STATE_RETURNED

	def test_borrowal_return_invalid(self, client: ClientWrapper):
		client.login(user_employee_Brno)

		# borrowal already ended
		resp = client.patch('/borrowals/%d/return' % borrowal_London_3.id, {})
		assert_error_response(resp)
