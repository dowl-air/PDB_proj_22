
from flask.testing import FlaskClient

from http import HTTPStatus
from json import loads

from helpers import (
	assert_error_response,
	find_by_id,
	protected_post, protected_put, protected_delete
)
from conftest import (
	book1984, bookBraveNewWorld,
	userCustomerCustomer
)

class TestReview:
	new_id: int = 0
	NEW_REVIEW_BOOK_ID = book1984.id

	def test_review_add(self, client: FlaskClient):
		USER = userCustomerCustomer

		data = {
			'title': '1984 Review',
			'content': 'Magnam neque quaerat sit tempora dolorem dolor numquam.',
			'rating': 7
		}

		resp = protected_post('/book/%d/review/add' % self.NEW_REVIEW_BOOK_ID, data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/book/%d/review' % self.NEW_REVIEW_BOOK_ID)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		review = find_by_id(self.new_id, json_data)
		assert review is not None
		assert review['title'] == data['title']
		assert review['content'] == data['content']
		assert review['rating'] == data['rating']
		customer = review['customer']
		assert customer['first_name'] == USER.first_name
		assert customer['last_name'] == USER.last_name
		assert customer['email'] == USER.email

	def test_review_add_invalid(self, client: FlaskClient):
		USER = userCustomerCustomer

		BOOK = bookBraveNewWorld

		template = {
			'title': 'Brave New World review',
			'content': 'Sed etincidunt dolor dolor sed voluptatem sed.',
			'rating': 9
		}

		# missing title
		data = template.copy()
		data['title'] = None
		resp = protected_post('/book/%d/review/add' % BOOK.id, data, client, USER)
		assert_error_response(resp)

		# invalid book id
		resp = protected_post('/book/%d/review/add' % 300, data, client, USER)
		assert_error_response(resp)

	def test_review_edit(self, client: FlaskClient):
		USER = userCustomerCustomer

		data = {
			'title': 'Edited review title',
			'content': 'Edited review content',
			'rating': 5
		}

		resp = protected_put('/review/%d/edit' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d/review' % self.NEW_REVIEW_BOOK_ID)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		review = find_by_id(self.new_id, json_data)
		assert review is not None
		assert review['title'] == data['title']
		assert review['content'] == data['content']
		assert review['rating'] == data['rating']

	def test_review_edit_invalid(self, client: FlaskClient):
		USER = userCustomerCustomer

		data = {
			'title': None,
			'content': 'Invalid edit - no title',
			'rating': 5
		}

		resp = protected_post('/review/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_review_delete(self, client: FlaskClient):
		USER = userCustomerCustomer

		resp = protected_delete('/review/%d/delete' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d/review' % self.NEW_REVIEW_BOOK_ID)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		review = find_by_id(self.new_id, json_data)
		assert review is None
