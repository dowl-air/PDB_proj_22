
from flask.testing import FlaskClient

from datetime import date
from http import HTTPStatus
from json import loads

from helpers import (
	assert_error_response,
	protected_post, protected_put, protected_delete
)
from conftest import (
	BOOK_COPY_STATE_GOOD, BOOK_COPY_STATE_DAMAGED,
	book1984, bookAnimalFarm,
	locationBrno, locationOlomouc,
	bc1984Brno1, bc1984London1, bc1984London2,
	userEmployeeBrno
)

class TestBookCopy:
	new_id: int = 0

	def test_book_copy_add(self, client: FlaskClient):
		LOCATION = locationBrno

		data = {
			'book_id': book1984.id,
			'location_id': LOCATION.id,
			'print_date': date(2019, 10, 5),
			'note': 'Note',
			'state': BOOK_COPY_STATE_GOOD
		}

		USER = userEmployeeBrno

		resp = protected_post('/book_copy/add', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/book_copy/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		copy = loads(resp.data.decode())
		assert copy['book_id'] == data['book_id']
		assert copy['print_date'] == data['print_date']
		assert copy['note'] == data['note']
		assert copy['state'] == data['state']
		location = copy['location']
		assert location['id'] == LOCATION.id
		assert location['name'] == LOCATION.name
		assert location['address'] == LOCATION.address

	def test_book_copy_add_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK = book1984
		LOCATION = locationBrno

		template = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': date(2019, 10, 5),
			'note': 'Note',
			'state': BOOK_COPY_STATE_GOOD
		}

		# missing book id
		data = template.copy()
		data['book_id'] = None
		resp = protected_post('/book_copy/add', data, client, USER)
		assert_error_response(resp)

		# missing location id
		data = template.copy()
		data['location_id'] = None
		resp = protected_post('/book_copy/add', data, client, USER)
		assert_error_response(resp)

		# missing print date
		data = template.copy()
		data['print_date'] = None
		resp = protected_post('/book_copy/add', data, client, USER)
		assert_error_response(resp)

	def test_book_copy_edit(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK = bookAnimalFarm
		LOCATION = locationOlomouc

		data = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': date(2018, 7, 20),
			'note': 'Edited note',
			'state': BOOK_COPY_STATE_DAMAGED
		}

		resp = protected_put('/book_copy/%d/edit' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book_copy/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		copy = loads(resp.data.decode())
		assert data['book_id'] == copy['book_id']
		assert data['print_date'] == copy['print_date']
		assert data['note'] == copy['note']
		assert data['state'] == copy['state']
		location = copy['location']
		assert location['id'] == LOCATION.id
		assert location['name'] == LOCATION.name
		assert location['address'] == LOCATION.address

	def test_book_copy_edit_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK = book1984
		LOCATION = locationBrno

		template = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': date(2019, 10, 5),
			'note': 'Note',
			'state': BOOK_COPY_STATE_GOOD
		}

		# missing book id
		data = template.copy()
		data['book_id'] = None
		resp = protected_post('/book_copy/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

		# missing location id
		data = template.copy()
		data['location_id'] = None
		resp = protected_post('/book_copy/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

		# missing print date
		data = template.copy()
		data['print_date'] = None
		resp = protected_post('/book_copy/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_book_copy_edit_propagation(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK_COPY = bc1984Brno1
		BOOK = bookAnimalFarm
		LOCATION = locationOlomouc

		data = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': date(2017, 4, 16),
			'note': 'Edited note',
			'state': BOOK_COPY_STATE_DAMAGED
		}

		resp = protected_put('/book_copy/%d/edit' % BOOK_COPY.id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		copies = book['book_copies']
		copies = list(filter(lambda x: x['id'] == BOOK_COPY.id, copies))
		assert len(copies) == 1
		copy = copies[0]
		assert copy['print_date'] == data['print_date']
		assert copy['note'] == data['note']
		assert copy['state'] == data['state']
		assert copy['location_id'] == LOCATION.id

	def test_book_copy_delete(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_delete('/book_copy/%d/delete' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book_copy/%d' % self.new_id)
		assert_error_response(resp)

	# cannot delete book copy with borrowals
	def test_book_copy_delete_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno
		BOOK_COPY = bc1984London1

		resp = protected_delete('/book_copy/%d/delete' % BOOK_COPY.id, client, USER)
		assert_error_response(resp)

	def test_book_copy_delete_propagation(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK_COPY = bc1984London2
		BOOK = book1984

		resp = protected_delete('/book_copy/%d/delete' % BOOK_COPY.id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		copies = list(filter(lambda x: x['id'] == BOOK_COPY.id, copies))
		assert len(copies) == 0
