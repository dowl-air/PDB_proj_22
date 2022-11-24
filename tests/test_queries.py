
from http import HTTPStatus
from json import loads

from helpers import ClientWrapper, to_json, assert_error_response
from data import (
	BOOKS, BOOK_COPIES, BORROWALS, RESERVATIONS, REVIEWS,
	BORROWAL_STATE_ACTIVE,
	BOOK_COPY_STATE_DELETED,
	book_1984, book_Hobbit, book_Good_Omens, book_Brave_New_World,
	bc_Hobbit_Brno, bc_Hobbit_London_1, bc_1984_Brno_1, bc_1984_Brno_2, bc_Animal_Farm_Brno,
	author_Orwell,
	category_comedy,
	location_London,
	user_customer_Customer, user_customer_Reviewer
)

def test_get_books(client: ClientWrapper):
	resp = client.get('/books')
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(BOOKS)

def test_get_book(client: ClientWrapper):
	BOOK = book_1984

	resp = client.get('/books/%d' % BOOK.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(BOOK)

def test_get_book_not_exists(client: ClientWrapper):
	resp = client.get('/books/300')
	assert_error_response(resp)

def test_get_book_copies(client: ClientWrapper):
	BOOK = book_Hobbit
	resp = client.get('/books/%d/book-copies/' % BOOK.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x.book_id == BOOK.id and x.state != BOOK_COPY_STATE_DELETED, BOOK_COPIES)))

def test_get_book_copy(client: ClientWrapper):
	BOOK_COPY = bc_Hobbit_London_1

	resp = client.get('/book-copies/%d' % BOOK_COPY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(BOOK_COPY)

def test_get_book_copy_borrowed_state_not_borrowed(client: ClientWrapper):
	BOOK_COPY = bc_Hobbit_Brno

	resp = client.get('/book-copies/%d/borrowed' % BOOK_COPY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'borrowed': False}

def test_get_book_copy_borrowed_state_borrowed(client: ClientWrapper):
	BOOK_COPY = bc_1984_Brno_1

	resp = client.get('/book-copies/%d/borrowed' % BOOK_COPY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'borrowed': True}

def test_get_book_copy_reserved_state_not_reserved(client: ClientWrapper):
	BOOK_COPY = bc_1984_Brno_2

	resp = client.get('/book-copies/%d/reserved' % BOOK_COPY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'reserved': False}

def test_get_book_copy_reserved_state_reserved(client: ClientWrapper):
	BOOK_COPY = bc_Animal_Farm_Brno

	resp = client.get('/book-copies/%d/reserved' % BOOK_COPY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'reserved': True}

def test_get_author(client: ClientWrapper):
	AUTHOR = author_Orwell

	resp = client.get('/authors/%d' % AUTHOR.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(AUTHOR)

def test_get_author_invalid(client: ClientWrapper):
	resp = client.get('/authors/300')
	assert_error_response(resp)

def test_get_category(client: ClientWrapper):
	CATEGORY = category_comedy

	resp = client.get('/categories/%d' % CATEGORY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(CATEGORY)

def test_get_category_not_exists(client: ClientWrapper):
	resp = client.get('/categories/300')
	assert_error_response(resp)

def test_get_location(client: ClientWrapper):
	LOCATION = location_London

	resp = client.get('/locations/%d' % LOCATION.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(LOCATION)

def test_get_location_not_exists(client: ClientWrapper):
	resp = client.get('/locations/300')
	assert_error_response(resp)

def test_get_profile(client: ClientWrapper):
	CUSTOMER = user_customer_Customer
	client.login(user=CUSTOMER)

	resp = client.get('/profile')
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(CUSTOMER)

def test_get_customer_borrowals(client: ClientWrapper):
	CUSTOMER = user_customer_Customer
	client.login(user=CUSTOMER)

	resp = client.get('/profile/borrowals')
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x.customer.id == CUSTOMER.id, BORROWALS)))

def test_get_customer_reservations(client: ClientWrapper):
	CUSTOMER = user_customer_Customer
	client.login(user=CUSTOMER)

	resp = client.get('/profile/reservations')
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x.customer.id == CUSTOMER.id, RESERVATIONS)))

def test_get_customer_reviews(client: ClientWrapper):
	CUSTOMER = user_customer_Reviewer
	client.login(user=CUSTOMER)

	resp = client.get('/profile/reviews')
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x.customer.id == CUSTOMER.id, REVIEWS)))

def test_get_reviews(client: ClientWrapper):
	BOOK = book_Good_Omens

	resp = client.get('/books/%d/reviews' % BOOK.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x['book_id'] == BOOK.id, REVIEWS)))

def test_get_reviews_none(client: ClientWrapper):
	BOOK = book_Brave_New_World

	resp = client.get('/books/%d/reviews' % BOOK.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json([])

def test_get_active_borrowals(client: ClientWrapper):
	resp = client.get('/active_borrowals')
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x.state == BORROWAL_STATE_ACTIVE, BORROWALS)))
