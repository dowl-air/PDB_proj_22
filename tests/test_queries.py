
from flask.testing import FlaskClient

from http import HTTPStatus
from json import loads

from helpers import entity_compare, expect_error, login, logout

from conftest import (
	BOOKS,
	book1984, bookHobbit, bookGoodOmens, bookBraveNewWorld,
	bcHobbitBrno, bcHobbitLondon1, bcHobbitLondon2, bcHobbitOlomouc,
	bc1984Brno1, bc1984Brno2, bcAnimalFarmBrno,
	authorOrwell,
	categoryComedy,
	locationLondon,
	userCustomerCustomer, userCustomerReviewer, userEmployeeBrno,
	borrowalLondon1, borrowalLondon3, borrowalBrno1, borrowalBrno2, borrowalBrnoActive1,
	reservationBrno, reservationBrnoActive,
	review1984, reviewAnimalFarm, reviewHobbit, reviewGoodOmens1, reviewGoodOmens2
)

def test_get_books(client: FlaskClient):
	resp = client.get('/books')
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, BOOKS)

def test_get_book(client: FlaskClient):
	resp = client.get('/books/%d' % book1984.id)
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, book1984)

def test_get_book_not_exists(client: FlaskClient):
	resp = client.get('/books/300')
	expect_error(resp)

def test_get_book_copies(client: FlaskClient):
	resp = client.get('/book_copies/book/%d' % bookHobbit.id)
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, [bcHobbitBrno, bcHobbitLondon1, bcHobbitLondon2, bcHobbitOlomouc])

def test_get_book_copy(client: FlaskClient):
	resp = client.get('/book_copies/%d' % bcHobbitLondon1.id)
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, bcHobbitLondon1)

def test_get_book_borrowed_state_not_borrowed(client: FlaskClient):
	resp = client.get('/book/%d/borrowed_state' % bcHobbitBrno.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'borrowed': False}

def test_get_book_borrowed_state_borrowed(client: FlaskClient):
	resp = client.get('/book/%d/borrowed_state' % bc1984Brno1.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'borrowed': True}

def test_get_book_reserved_state_not_reserved(client: FlaskClient):
	resp = client.get('/book/%d/reserved_state' % bc1984Brno2.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'reserved': False}

def test_get_book_reserved_state_reserved(client: FlaskClient):
	resp = client.get('/book/%d/reserved_state' % bcAnimalFarmBrno.id)
	assert resp.status_code == HTTPStatus.OK
	assert loads(resp.data.decode()) == {'reserved': True}

def test_get_author(client: FlaskClient):
	resp = client.get('/author/%d' % authorOrwell.id)
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, authorOrwell)

def test_get_author_not_exists(client: FlaskClient):
	resp = client.get('/author/300')
	expect_error(resp)

def test_get_category(client: FlaskClient):
	resp = client.get('/category/%d' % categoryComedy.id)
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, categoryComedy)

def test_get_category_not_exists(client: FlaskClient):
	resp = client.get('/category/300')
	expect_error(resp)

def test_get_location(client: FlaskClient):
	resp = client.get('/location/%d' % locationLondon.id)
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, locationLondon)

def test_get_location_not_exists(client: FlaskClient):
	resp = client.get('/location/300')
	expect_error(resp)

def test_get_profile(client: FlaskClient):
	login(client, userCustomerCustomer.email, 'customer') # TODO

	resp = client.get('/profile/%d' % userCustomerCustomer.id) # TODO
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, userCustomerCustomer)

	logout(client)

def test_get_borrowals(client: FlaskClient):
	login(client, userCustomerCustomer.email, 'customer') # TODO

	resp = client.get('/profile/borrowals/%d' % userCustomerCustomer.id) # TODO
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, [borrowalLondon1, borrowalLondon3, borrowalBrno1, borrowalBrno2])

	logout(client)

def test_get_reservations(client: FlaskClient):
	login(client, userCustomerCustomer.email, 'customer') # TODO

	resp = client.get('/profile/reservations/%d' % userCustomerCustomer.id) # TODO
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, [reservationBrno, reservationBrnoActive])

	logout(client)

def test_get_reviews(client: FlaskClient):
	login(client, userCustomerReviewer.email, 'reviewer') # TODO

	resp = client.get('/profile/reviews/%d' % userCustomerReviewer.id) # TODO
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, [review1984, reviewAnimalFarm, reviewHobbit, reviewGoodOmens1])

	logout(client)

def test_get_reviews(client: FlaskClient):
	resp = client.get('/reviews/book/%d' % bookGoodOmens.id) # TODO
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, [reviewGoodOmens1, reviewGoodOmens2])

def test_get_reviews_none(client: FlaskClient):
	resp = client.get('/reviews/book/%d' % bookBraveNewWorld.id) # TODO
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, [])

def test_get_active_borrowals(client: FlaskClient):
	login(client, userEmployeeBrno.email, 'brno') # TODO

	resp = client.get('/active_borrowals')
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, [borrowalBrnoActive1])

	logout(client)
