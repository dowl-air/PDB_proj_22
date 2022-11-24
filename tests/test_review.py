
from http import HTTPStatus
from json import loads

from helpers import (
	ClientWrapper,
	assert_error_response,
	find_by_id
)
from data import (
	book_1984, book_Brave_New_World,
	user_customer_Customer
)

class TestReview:
	new_id: int = 0
	NEW_REVIEW_BOOK_ID = book_1984.id

	def test_review_add(self, client: ClientWrapper):
		USER = user_customer_Customer
		client.login(user=USER)

		data = {
			'title': '1984 Review',
			'content': 'Magnam neque quaerat sit tempora dolorem dolor numquam.',
			'rating': 7
		}

		resp = client.post('/books/%d/reviews' % TestReview.NEW_REVIEW_BOOK_ID, data)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		TestReview.new_id = json_data['id']

		resp = client.get('/books/%d/reviews' % TestReview.NEW_REVIEW_BOOK_ID)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		review = find_by_id(TestReview.new_id, json_data)
		assert review is not None
		assert review['title'] == data['title']
		assert review['content'] == data['content']
		assert review['rating'] == data['rating']
		customer = review['customer']
		assert customer['first_name'] == USER.first_name
		assert customer['last_name'] == USER.last_name
		assert customer['email'] == USER.email

		resp = client.get('/profile/reviews')
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		review = find_by_id(TestReview.new_id, json_data)
		assert review is not None
		assert review['title'] == data['title']
		assert review['content'] == data['content']
		assert review['rating'] == data['rating']

	def test_review_add_invalid(self, client: ClientWrapper):
		client.login(user=user_customer_Customer)

		BOOK = book_Brave_New_World

		template = {
			'title': 'Brave New World review',
			'content': 'Sed etincidunt dolor dolor sed voluptatem sed.',
			'rating': 9
		}

		# missing title
		data = template.copy()
		data['title'] = None
		resp = client.post('/books/%d/reviews' % BOOK.id, data)
		assert_error_response(resp)

		# invalid book id
		resp = client.post('/books/%d/reviews' % 300, data)
		assert_error_response(resp)

	def test_review_edit(self, client: ClientWrapper):
		client.login(user=user_customer_Customer)

		data = {
			'title': 'Edited review title',
			'content': 'Edited review content',
			'rating': 5
		}

		resp = client.put('/reviews/%d' % TestReview.new_id, data)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/books/%d/reviews' % TestReview.NEW_REVIEW_BOOK_ID)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		review = find_by_id(TestReview.new_id, json_data)
		assert review is not None
		assert review['title'] == data['title']
		assert review['content'] == data['content']
		assert review['rating'] == data['rating']

	def test_review_edit_invalid(self, client: ClientWrapper):
		client.login(user=user_customer_Customer)

		data = {
			'title': None,
			'content': 'Invalid edit - no title',
			'rating': 5
		}

		resp = client.put('/reviews/%d' % TestReview.new_id, data)
		assert_error_response(resp)

	def test_review_delete(self, client: ClientWrapper):
		client.login(user=user_customer_Customer)

		resp = client.delete('/reviews/%d' % TestReview.new_id, {})
		assert resp.status_code == HTTPStatus.OK

		# delete propagation
		resp = client.get('/books/%d/reviews' % TestReview.NEW_REVIEW_BOOK_ID)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		review = find_by_id(TestReview.new_id, json_data)
		assert review is None

		resp = client.get('/profile/reviews')
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		review = find_by_id(TestReview.new_id, json_data)
		assert review is None
