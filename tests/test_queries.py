
from flask.testing import FlaskClient

from http import HTTPStatus
from json import loads

from helpers import to_json, assert_error_response
from conftest import (
	BOOKS, BOOK_COPIES, BORROWALS, RESERVATIONS, REVIEWS,
	BORROWAL_STATE_ACTIVE,
	book1984, bookHobbit, bookGoodOmens, bookBraveNewWorld,
	bcHobbitBrno, bcHobbitLondon1, bc1984Brno1, bc1984Brno2, bcAnimalFarmBrno,
	authorOrwell,
	categoryComedy,
	locationLondon,
	userCustomerCustomer, userCustomerReviewer
)

def test_get_books(client: FlaskClient):
	resp = client.get('/books')
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(BOOKS)

def test_get_book(client: FlaskClient):
	BOOK = book1984

	resp = client.get('/books/%d' % BOOK.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(BOOK)

def test_get_book_not_exists(client: FlaskClient):
	resp = client.get('/books/300')
	assert_error_response(resp)

def test_get_book_copies(client: FlaskClient):
	BOOK = bookHobbit
	resp = client.get('/books/%d/book-copies/' % BOOK.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x.book_id == BOOK.id, BOOK_COPIES)))

def test_get_book_copy(client: FlaskClient):
	BOOK_COPY = bcHobbitLondon1

	resp = client.get('/book-copies/%d' % BOOK_COPY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(BOOK_COPY)

def test_get_book_copy_borrowed_state_not_borrowed(client: FlaskClient):
	BOOK_COPY = bcHobbitBrno

	resp = client.get('/book-copies/%d/borrowed' % BOOK_COPY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'borrowed': False}

def test_get_book_copy_borrowed_state_borrowed(client: FlaskClient):
	BOOK_COPY = bc1984Brno1

	resp = client.get('/book-copies/%d/borrowed' % BOOK_COPY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'borrowed': True}

def test_get_book_copy_reserved_state_not_reserved(client: FlaskClient):
	BOOK_COPY = bc1984Brno2

	resp = client.get('/book-copies/%d/reserved' % BOOK_COPY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'reserved': False}

def test_get_book_copy_reserved_state_reserved(client: FlaskClient):
	BOOK_COPY = bcAnimalFarmBrno

	resp = client.get('/book-copies/%d/reserved' % BOOK_COPY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'reserved': True}

def test_get_author(client: FlaskClient):
	AUTHOR = authorOrwell

	resp = client.get('/authors/%d' % AUTHOR.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(AUTHOR)

def test_get_author_invalid(client: FlaskClient):
	resp = client.get('/authors/300')
	assert_error_response(resp)

def test_get_category(client: FlaskClient):
	CATEGORY = categoryComedy

	resp = client.get('/categories/%d' % CATEGORY.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(CATEGORY)

def test_get_category_not_exists(client: FlaskClient):
	resp = client.get('/categories/300')
	assert_error_response(resp)

def test_get_location(client: FlaskClient):
	LOCATION = locationLondon

	resp = client.get('/locations/%d' % LOCATION.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(LOCATION)

def test_get_location_not_exists(client: FlaskClient):
	resp = client.get('/locations/300')
	assert_error_response(resp)

def test_get_profile(client: FlaskClient):
	CUSTOMER = userCustomerCustomer

	resp = client.get('/profile/%d' % CUSTOMER.id) # TODO
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(CUSTOMER)

def test_get_customer_borrowals(client: FlaskClient):
	CUSTOMER = userCustomerCustomer

	resp = client.get('/profile/%d/borrowals' % CUSTOMER.id) # TODO
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x.customer.id == CUSTOMER.id, BORROWALS)))

def test_get_customer_reservations(client: FlaskClient):
	CUSTOMER = userCustomerCustomer

	resp = client.get('/profile/%d/reservations' % CUSTOMER.id) # TODO
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x.customer.id == CUSTOMER.id, RESERVATIONS)))

def test_get_customer_reviews(client: FlaskClient):
	CUSTOMER = userCustomerReviewer

	resp = client.get('/profile/%d/reviews' % CUSTOMER.id) # TODO
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x.customer.id == CUSTOMER.id, REVIEWS)))

def test_get_reviews(client: FlaskClient):
	BOOK = bookGoodOmens

	resp = client.get('/books/%d/reviews' % BOOK.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x['book_id'] == BOOK.id, REVIEWS)))

def test_get_reviews_none(client: FlaskClient):
	BOOK = bookBraveNewWorld

	resp = client.get('/books/%d/reviews' % BOOK.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json([])

def test_get_active_borrowals(client: FlaskClient):
	resp = client.get('/active_borrowals')
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == to_json(list(filter(lambda x: x.state == BORROWAL_STATE_ACTIVE, BORROWALS)))
