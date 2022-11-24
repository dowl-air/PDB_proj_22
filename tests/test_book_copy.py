
from datetime import date
from http import HTTPStatus
from json import loads

from helpers import (
	ClientWrapper,
	assert_error_response,
	format_date
)
from data import (
	BOOK_COPY_STATE_GOOD, BOOK_COPY_STATE_DAMAGED,
	book_1984, book_Animal_Farm,
	location_Brno, location_Olomouc,
	bc_1984_Brno_1, bc_1984_London_1, bc_1984_London_2,
	user_employee_Brno
)

class TestBookCopy:
	new_id: int = 0

	def test_book_copy_add(self, client: ClientWrapper):
		client.login(user=user_employee_Brno)

		LOCATION = location_Brno
		BOOK = book_1984

		data = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': format_date(date(2019, 10, 5)),
			'note': 'Note',
			'state': BOOK_COPY_STATE_GOOD
		}

		resp = client.post('/book-copies', data)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/book-copies/%d' % self.new_id)
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

	def test_book_copy_add_invalid(self, client: ClientWrapper):
		client.login(user=user_employee_Brno)

		BOOK = book_1984
		LOCATION = location_Brno

		template = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': format_date(date(2019, 10, 5)),
			'note': 'Note',
			'state': BOOK_COPY_STATE_GOOD
		}

		# missing book id
		data = template.copy()
		data['book_id'] = None
		resp = client.post('/book_copies', data)
		assert_error_response(resp)

		# missing location id
		data = template.copy()
		data['location_id'] = None
		resp = client.post('/book_copies', data)
		assert_error_response(resp)

		# missing print date
		data = template.copy()
		data['print_date'] = None
		resp = client.post('/book_copies', data)
		assert_error_response(resp)

	def test_book_copy_edit(self, client: ClientWrapper):
		client.login(user=user_employee_Brno)

		BOOK = book_Animal_Farm
		LOCATION = location_Olomouc

		data = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': format_date(date(2018, 7, 20)),
			'note': 'Edited note',
			'state': BOOK_COPY_STATE_DAMAGED
		}

		resp = client.put('/book-copies/%d' % self.new_id, data)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book-copies/%d' % self.new_id)
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

	def test_book_copy_edit_invalid(self, client: ClientWrapper):
		client.login(user=user_employee_Brno)

		BOOK = book_1984
		LOCATION = location_Brno

		template = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': format_date(date(2019, 10, 5)),
			'note': 'Note',
			'state': BOOK_COPY_STATE_GOOD
		}

		# missing book id
		data = template.copy()
		data['book_id'] = None
		resp = client.put('/book-copies/%d' % self.new_id, data)
		assert_error_response(resp)

		# missing location id
		data = template.copy()
		data['location_id'] = None
		resp = client.put('/book-copies/%d' % self.new_id, data)
		assert_error_response(resp)

		# missing print date
		data = template.copy()
		data['print_date'] = None
		resp = client.put('/book-copies/%d' % self.new_id, data)
		assert_error_response(resp)

	def test_book_copy_edit_propagation(self, client: ClientWrapper):
		client.login(user=user_employee_Brno)

		BOOK_COPY = bc_1984_Brno_1
		BOOK = book_Animal_Farm
		LOCATION = location_Olomouc

		data = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': format_date(date(2017, 4, 16)),
			'note': 'Edited note',
			'state': BOOK_COPY_STATE_DAMAGED
		}

		resp = client.put('/book-copies/%d' % BOOK_COPY.id, data)
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

	def test_book_copy_delete(self, client: ClientWrapper):
		client.login(user=user_employee_Brno)

		resp = client.delete('/book-copies/%d' % self.new_id, {})
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book-copies/%d' % self.new_id)
		assert_error_response(resp)

	# cannot delete book copy with borrowals
	def test_book_copy_delete_invalid(self, client: ClientWrapper):
		client.login(user=user_employee_Brno)

		BOOK_COPY = bc_1984_London_1

		resp = client.delete('/book-copies/%d' % BOOK_COPY.id, {})
		assert_error_response(resp)

	def test_book_copy_delete_propagation(self, client: ClientWrapper):
		client.login(user=user_employee_Brno)

		BOOK_COPY = bc_1984_London_2
		BOOK = book_1984

		resp = client.delete('/book-copies/%d' % BOOK_COPY.id, {})
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		copies = list(filter(lambda x: x['id'] == BOOK_COPY.id, book['copies']))
		assert len(copies) == 0
