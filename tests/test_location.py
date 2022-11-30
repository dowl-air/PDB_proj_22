
from http import HTTPStatus
from json import loads

from helpers import ClientWrapper, assert_error_response
from data import (
    location_Brno,
    bc_1984_Brno_2,
    user_admin_Admin
)


class TestLocation:
    new_id: int = 0

    def test_location_add(self, client: ClientWrapper):
        client.login(user=user_admin_Admin)

        data = {
            'name': 'VUT FIT',
            'address': 'Božetěchova 1/2, 612 00 Brno-Královo Pole'
        }

        resp = client.post('/locations', data)
        assert resp.status_code == HTTPStatus.CREATED
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        TestLocation.new_id = json_data['id']

        resp = client.get('/locations/%d' % TestLocation.new_id)
        assert resp.status_code == HTTPStatus.OK
        location = loads(resp.data.decode())
        assert data['name'] == location['name']
        assert data['address'] == location['address']

    def test_location_add_invalid(self, client: ClientWrapper):
        client.login(user=user_admin_Admin)

        data = {
            'address': 'Missing location name'
        }

        resp = client.post('/locations', data)
        assert_error_response(resp)

    def test_location_edit(self, client: ClientWrapper):
        client.login(user=user_admin_Admin)

        data = {
            'name': 'Edited VUT FIT location',
            'address': 'Edited location address'
        }

        resp = client.put('/locations/%d' % TestLocation.new_id, data)
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/locations/%d' % TestLocation.new_id)
        assert resp.status_code == HTTPStatus.OK
        location = loads(resp.data.decode())
        assert data['name'] == location['name']
        assert data['address'] == location['address']

    def test_location_edit_invalid(self, client: ClientWrapper):
        client.login(user=user_admin_Admin)

        data = {
            'name': None,
            'description': 'Invalid edit - no name'
        }

        resp = client.put('/locations/%d' % TestLocation.new_id, data)
        assert_error_response(resp)

    def test_location_edit_propagation(self, client: ClientWrapper):
        client.login(user=user_admin_Admin)

        data = {
            'name': 'Ostrava',
            'address': 'idk'
        }

        LOCATION = location_Brno
        BOOK_COPY = bc_1984_Brno_2

        resp = client.put('/locations/%d' % LOCATION.id, data)
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/book-copies/%d' % BOOK_COPY.id)
        assert resp.status_code == HTTPStatus.OK
        book_copy = loads(resp.data.decode())
        assert book_copy['location']['name'] == data['name']
        assert book_copy['location']['address'] == data['address']

    def test_location_delete(self, client: ClientWrapper):
        client.login(user=user_admin_Admin)

        resp = client.delete('/locations/%d' % TestLocation.new_id, {})
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/locations/%d' % TestLocation.new_id)
        assert_error_response(resp)

    # cannot delete location with assigned book copies
    def test_location_delete_invalid(self, client: ClientWrapper):
        client.login(user=user_admin_Admin)

        LOCATION = location_Brno

        resp = client.delete('/locations/%d' % LOCATION.id, {})
        assert_error_response(resp)
