
from datetime import date
from http import HTTPStatus
from json import loads

from app.entity import ReservationState

from helpers import (
    ClientWrapper,
    assert_error_response, assert_ok_created,
    find_by_id,
    format_date
)
from data import (
    BORROWAL_STATE_ACTIVE, BORROWAL_STATE_RETURNED,

    bc_1984_Brno_1, bc_Animal_Farm_Brno, bc_Hobbit_Olomouc, bc_Brave_New_World_Brno,
    bc_Hobbit_London_1, bc_Hobbit_London_2, bc_1984_London_3, bc_Animal_Farm_Olomouc,

    user_employee_Brno, user_customer_Customer, user_employee_London, user_customer_Smith,
    borrowal_London_3,
    reservation_London_active_1,
    reservation_London_active_2
)


class TestBorrowal:
    new_id: int = 0

    def test_borrowal_add(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        BOOK_COPY = bc_Hobbit_Olomouc
        CUSTOMER = user_customer_Customer

        data = {
            'book_copy_id': BOOK_COPY.id,
            'customer_id': CUSTOMER.id
        }

        resp = client.post('/borrowals', data)
        assert_ok_created(resp.status_code)
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        TestBorrowal.new_id = json_data['id']

        client.login(user=CUSTOMER)

        resp = client.get('/profile/borrowals')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        borrowal = find_by_id(TestBorrowal.new_id, json_data)
        assert borrowal is not None
        assert 'book_copy' in borrowal and borrowal['book_copy']['id'] == BOOK_COPY.id
        assert borrowal['start_date'] == format_date(date.today())
        assert borrowal['state'] == BORROWAL_STATE_ACTIVE

    def test_borrowal_add_invalid_reserved(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        BOOK_COPY = bc_Hobbit_London_2  # active reservation by a different customer
        CUSTOMER = user_customer_Customer

        data = {
            'book_copy_id': BOOK_COPY.id,
            'customer_id': CUSTOMER.id
        }

        resp = client.post('/borrowals', data)
        assert_error_response(resp)

    def test_borrowal_add_invalid_borrowed(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        BOOK_COPY = bc_1984_Brno_1  # borrowed (by a different customer)
        CUSTOMER = user_customer_Customer

        data = {
            'book_copy_id': BOOK_COPY.id,
            'customer_id': CUSTOMER.id
        }

        resp = client.post('/borrowals', data)
        assert_error_response(resp)

    def test_borrowal_add_invalid_borrowed_expired(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        BOOK_COPY = bc_Brave_New_World_Brno  # expired borrowal (by a different customer)
        CUSTOMER = user_customer_Customer

        data = {
            'book_copy_id': BOOK_COPY.id,
            'customer_id': CUSTOMER.id
        }

        resp = client.post('/borrowals', data)
        assert_error_response(resp)

    # cannot borrow deleted book copy
    def test_borrowal_add_invalid_deleted(self, client: ClientWrapper):
        client.login(user=user_employee_London)

        BOOK_COPY = bc_1984_London_3  # deleted book copy
        CUSTOMER = user_customer_Customer

        data = {
            'book_copy_id': BOOK_COPY.id,
            'customer_id': CUSTOMER.id
        }

        resp = client.post('/borrowals', data)
        assert_error_response(resp)

    def test_borrowal_add_valid_reservation_expired(self, client: ClientWrapper):
        client.login(user=user_employee_London)

        BOOK_COPY = bc_Animal_Farm_Olomouc  # reserved by customer 'Smith'
        CUSTOMER = user_customer_Customer

        data = {
            'book_copy_id': BOOK_COPY.id,
            'customer_id': CUSTOMER.id
        }

        resp = client.post('/borrowals', data)
        assert_ok_created(resp.status_code)
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        TestBorrowal.new_id = json_data['id']

        client.login(user=CUSTOMER)

        resp = client.get('/profile/borrowals')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        borrowal = find_by_id(TestBorrowal.new_id, json_data)
        assert borrowal is not None
        assert 'book_copy' in borrowal and borrowal['book_copy']['id'] == BOOK_COPY.id
        assert borrowal['start_date'] == format_date(date.today())
        assert borrowal['state'] == BORROWAL_STATE_ACTIVE

    def test_borrowal_add_valid_reserved(self, client: ClientWrapper):
        client.login(user=user_employee_London)

        BOOK_COPY = bc_Hobbit_London_2
        RESERVATION = reservation_London_active_2
        CUSTOMER = user_customer_Smith

        data = {
            'book_copy_id': BOOK_COPY.id,
            'customer_id': CUSTOMER.id
        }

        resp = client.post('/borrowals', data)
        assert_ok_created(resp.status_code)
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        TestBorrowal.new_id = json_data['id']

        client.login(user=CUSTOMER)

        resp = client.get('/profile/borrowals')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        borrowal = find_by_id(TestBorrowal.new_id, json_data)
        assert borrowal is not None
        assert 'book_copy' in borrowal and borrowal['book_copy']['id'] == BOOK_COPY.id
        assert borrowal['start_date'] == format_date(date.today())
        assert borrowal['state'] == BORROWAL_STATE_ACTIVE

        # reservation has been closed
        resp = client.get('/profile/reservations')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        reservation = find_by_id(RESERVATION.id, json_data)
        assert reservation is not None
        assert 'book_copy' in reservation and reservation['book_copy']['id'] == BOOK_COPY.id
        assert reservation['state'] == ReservationState.CLOSED

    def test_borrowal_return(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        resp = client.patch('/borrowals/%d/return' % TestBorrowal.new_id, {})
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/active-borrowals')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        borrowal = find_by_id(TestBorrowal.new_id, json_data)
        assert borrowal is None  # active-borrowals only return active ones
        #assert borrowal['state'] == BORROWAL_STATE_RETURNED

    def test_borrowal_return_invalid(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        # borrowal already ended
        resp = client.patch('/borrowals/%d/return' % borrowal_London_3.id, {})
        assert_error_response(resp)
