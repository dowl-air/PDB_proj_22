
from datetime import date
from http import HTTPStatus
from json import loads

from app.entity import BookCopyState, ReservationState

from helpers import (
    ClientWrapper,
    assert_ok_created, assert_error_response,
    find_by_id, format_date
)
from data import (
    BORROWAL_STATE_ACTIVE, BORROWAL_STATE_RETURNED,
    bc_Animal_Farm_London, bc_Good_Omens_Brno,
    user_employee_London, user_customer_Customer, user_customer_Smith, user_employee_Brno,
    location_Brno
)


class TestScenarios:
    def test_register_borrow(self, client: ClientWrapper):
        # register new customer
        NEW_CUSTOMER = {
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'test@customer.cz',
            'password': 'testPass147'
        }

        resp = client.post('/register', NEW_CUSTOMER)
        assert_ok_created(resp.status_code)
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        NEW_CUSTOMER_ID = json_data['id']

        # borrow book copy as new customer
        BOOK_COPY = bc_Animal_Farm_London
        EMPLOYEE = user_employee_London

        client.login(user=EMPLOYEE)

        data = {
            'book_copy_id': BOOK_COPY.id,
            'customer_id': NEW_CUSTOMER_ID
        }

        resp = client.post('/borrowals', data)
        assert resp.status_code == HTTPStatus.CREATED
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        NEW_BORROWAL_ID = json_data['id']

        client.login(email=NEW_CUSTOMER['email'], password=NEW_CUSTOMER['password'])

        resp = client.get('/profile/borrowals')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        borrowal = find_by_id(NEW_BORROWAL_ID, json_data)
        assert borrowal is not None
        assert 'book_copy' in borrowal and borrowal['book_copy']['id'] == BOOK_COPY.id
        assert borrowal['start_date'] == format_date(date.today())
        assert borrowal['state'] == BORROWAL_STATE_ACTIVE

        # return borrowed book copy
        client.login(user=EMPLOYEE)

        resp = client.patch('/borrowals/%d/return' % NEW_BORROWAL_ID, {})
        assert resp.status_code == HTTPStatus.OK

        client.login(email=NEW_CUSTOMER['email'], password=NEW_CUSTOMER['password'])

        resp = client.get('/profile/borrowals')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        borrowal = find_by_id(NEW_BORROWAL_ID, json_data)
        assert borrowal is not None
        assert borrowal['state'] == BORROWAL_STATE_RETURNED

    def test_reserve_borrow(self, client: ClientWrapper):
        # reserve book copy as customer
        CUSTOMER = user_customer_Customer
        client.login(user=CUSTOMER)

        BOOK_COPY = bc_Good_Omens_Brno

        data = {
            'book_copy_id': BOOK_COPY.id
        }

        resp = client.post('/reservations', data)
        assert resp.status_code == HTTPStatus.CREATED
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        NEW_RESERVATION_ID = json_data['id']

        resp = client.get('/profile/reservations')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        reservation = find_by_id(NEW_RESERVATION_ID, json_data)
        assert reservation is not None
        assert 'book_copy' in reservation and reservation['book_copy']['id'] == BOOK_COPY.id
        assert reservation['start_date'] == format_date(date.today())
        assert reservation['state'] == ReservationState.ACTIVE.value

        # cannot reserve book as other customer
        OTHER_CUSTOMER = user_customer_Smith

        client.login(user=OTHER_CUSTOMER)

        data = {
            'book_copy_id': BOOK_COPY.id
        }

        resp = client.post('/reservations', data)
        assert_error_response(resp)

        # cannot borrow book as other customer
        EMPLOYEE = user_employee_Brno

        client.login(user=EMPLOYEE)

        data = {
            'book_copy_id': BOOK_COPY.id,
            'customer_id': OTHER_CUSTOMER.id
        }

        resp = client.post('/borrowals', data)
        assert_error_response(resp)

        # borrow book as original customer
        data = {
            'book_copy_id': BOOK_COPY.id,
            'customer_id': CUSTOMER.id
        }

        resp = client.post('/borrowals', data)
        assert resp.status_code == HTTPStatus.CREATED
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        NEW_BORROWAL_ID = json_data['id']

        client.login(user=CUSTOMER)

        resp = client.get('/profile/borrowals')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        borrowal = find_by_id(NEW_BORROWAL_ID, json_data)
        borrowal is not None
        assert 'book_copy' in borrowal and borrowal['book_copy']['id'] == BOOK_COPY.id
        assert borrowal['start_date'] == format_date(date.today())
        assert borrowal['state'] == BORROWAL_STATE_ACTIVE

        resp = client.get('/profile/reservations')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        reservation = find_by_id(NEW_RESERVATION_ID, json_data)
        assert reservation is not None
        assert reservation['state'] == ReservationState.CLOSED.value

    # add new book with new associated entities (author, category...)
    def test_add_new_book(self, client: ClientWrapper):
        LOCATION = location_Brno

        # add new author
        client.login(user=user_employee_Brno)

        NEW_AUTHOR = {
            'first_name': 'Franz',
            'last_name': 'Kafka',
            'description': 'German-speaking Bohemian novelist and short-story writer, widely regarded...'
        }

        resp = client.post('/authors', NEW_AUTHOR)
        assert_ok_created(resp.status_code)
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        NEW_AUTHOR_ID = json_data['id']

        # add new category
        NEW_CATEGORY = {
            'name': 'Absurdist fiction',
            'description': 'Genre that focuses on the experiences of characters in situations where they cannot find...'
        }

        resp = client.post('/categories', NEW_CATEGORY)
        assert_ok_created(resp.status_code)
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        NEW_CATEGORY_ID = json_data['id']

        # add new book
        NEW_BOOK = {
            'name': 'The Trial',
            'ISBN': '978-1-78950-889-5',
            'release_date': format_date(date(1925, 1, 1)),
            'description': "One of Kafka's best known works, it tells the story of Josef K., a man arrested and prosecuted...",
            'authors': [NEW_AUTHOR_ID],
            'categories': [NEW_CATEGORY_ID]
        }

        resp = client.post('/books', NEW_BOOK)
        assert_ok_created(resp.status_code)
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        NEW_BOOK_ID = json_data['id']

        # add new book copy
        NEW_BOOK_COPY = {
            'book_id': NEW_BOOK_ID,
            'location_id': LOCATION.id,
            'print_date': format_date(date(2020, 5, 12)),
            'note': 'Book copy note',
            'state': BookCopyState.GOOD.value
        }

        resp = client.post('/book-copies', NEW_BOOK_COPY)
        assert resp.status_code == HTTPStatus.CREATED
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        NEW_BOOK_COPY_ID = json_data['id']

        # check the newly added book
        resp = client.get('/books/%d' % NEW_BOOK_ID)
        assert resp.status_code == HTTPStatus.OK
        book = loads(resp.data.decode())
        assert book['name'] == NEW_BOOK['name']
        assert book['ISBN'] == NEW_BOOK['ISBN']
        assert book['release_date'] == NEW_BOOK['release_date']
        assert book['description'] == NEW_BOOK['description']
        assert len(book['authors']) == 1
        author = book['authors'][0]
        assert author['id'] == NEW_AUTHOR_ID
        assert author['first_name'] == NEW_AUTHOR['first_name']
        assert author['last_name'] == NEW_AUTHOR['last_name']
        assert len(book['categories']) == 1
        category = book['categories'][0]
        assert category['id'] == NEW_CATEGORY_ID
        assert category['name'] == NEW_CATEGORY['name']
        assert category['description'] == NEW_CATEGORY['description']
        assert len(book['book_copies']) == 1
        copy = book['book_copies'][0]
        assert copy['id'] == NEW_BOOK_COPY_ID
        assert copy['print_date'] == NEW_BOOK_COPY['print_date']
        assert copy['note'] == NEW_BOOK_COPY['note']
        assert copy['state'] == NEW_BOOK_COPY['state']
        assert copy['location_id'] == NEW_BOOK_COPY['location_id']

        # check that author has the book
        resp = client.get('/authors/%d' % NEW_AUTHOR_ID)
        assert resp.status_code == HTTPStatus.OK
        author = loads(resp.data.decode())
        assert len(author['books']) == 1
        book = author['books'][0]
        assert book['name'] == NEW_BOOK['name']
        assert book['ISBN'] == NEW_BOOK['ISBN']
        assert book['release_date'] == NEW_BOOK['release_date']
        assert book['description'] == NEW_BOOK['description']
