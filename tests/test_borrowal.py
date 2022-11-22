
from flask.testing import FlaskClient

from datetime import date
from http import HTTPStatus
from json import loads

from helpers import (
	assert_error_response,
	find_by_id,
	protected_post, protected_patch
)
from conftest import (
	BORROWAL_STATE_ACTIVE, BORROWAL_STATE_RETURNED,
	bc1984Brno1, bcAnimalFarmBrno, bcHobbitOlomouc,
	userEmployeeBrno, userCustomerCustomer,
	borrowalLondon3
)

class TestBorrowal:
	new_id: int = 0

	def test_borrowal_add(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK_COPY = bcHobbitOlomouc
		CUSTOMER = userCustomerCustomer

		data = {
			'book_copy_id': BOOK_COPY.id,
			'customer_id': CUSTOMER.id
		}

		resp = protected_post('/borrowal/add', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/profile/%d/borrowals' % CUSTOMER.id)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		borrowal = find_by_id(self.new_id, json_data)
		assert borrowal['book_copy_id'] == BOOK_COPY.id
		assert borrowal['start_date'] == date.today()
		assert borrowal['state'] == BORROWAL_STATE_ACTIVE

	def test_borrowal_add_invalid_reserved(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK_COPY = bcAnimalFarmBrno
		CUSTOMER = userCustomerCustomer

		data = {
			'book_copy_id': BOOK_COPY.id,
			'customer_id': CUSTOMER.id
		}

		resp = protected_post('/borrowal/add', data, client, USER)
		assert_error_response(resp)

	def test_borrowal_add_invalid_borrowed(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK_COPY = bc1984Brno1
		CUSTOMER = userCustomerCustomer

		data = {
			'book_copy_id': BOOK_COPY.id,
			'customer_id': CUSTOMER.id
		}

		resp = protected_post('/borrowal/add', data, client, USER)
		assert_error_response(resp)

	def test_borrowal_return(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_patch('/borrowal/%d/return' % self.new_id, {}, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/active_borrowals')
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		borrowal = find_by_id(self.new_id, json_data)
		assert borrowal is not None
		assert borrowal['state'] == BORROWAL_STATE_RETURNED

	def test_borrowal_return_invalid(self, client: FlaskClient):
		USER = userCustomerCustomer

		# borrowal already ended
		resp = protected_patch('/borrowal/%d/return' % borrowalLondon3.id, {}, client, USER)
		assert_error_response(resp)
