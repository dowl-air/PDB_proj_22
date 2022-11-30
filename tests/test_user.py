
from http import HTTPStatus
from json import loads

from helpers import ClientWrapper, assert_error_response
from data import user_customer_Customer


class TestUser:
    NEW_USER = {
        'id': 0,
        'first_name': 'First',
        'last_name': 'Last',
        'email': 'new_email@email.cz',
        'password': 'password123'
    }
    token: str = ''

    def test_register(self, client: ClientWrapper):
        data = {
            'first_name': TestUser.NEW_USER['first_name'],
            'last_name': TestUser.NEW_USER['last_name'],
            'email': TestUser.NEW_USER['email'],
            'password': TestUser.NEW_USER['password']
        }

        resp = client.post('/register', data)
        assert resp.status_code == HTTPStatus.CREATED
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        TestUser.NEW_USER['id'] = json_data['id']

    def test_register_invalid(self, client: ClientWrapper):
        template = {
            'first_name': 'Invalid',
            'last_name': 'Registration',
            'email': 'another_email@email.cz',
            'password': '123password'
        }

        # missing email
        data = template.copy()
        data['email'] = None
        resp = client.post('/register', data)
        assert_error_response(resp)

        # duplicate email
        data = template.copy()
        data['email'] = TestUser.NEW_USER['email']
        resp = client.post('/register', data)
        assert_error_response(resp)

        # missing password
        data = template.copy()
        data['password'] = None
        resp = client.post('/register', data)
        assert_error_response(resp)

    def test_login(self, client: ClientWrapper):
        data = {
            'email': TestUser.NEW_USER['email'],
            'password': TestUser.NEW_USER['password']
        }

        resp = client.post('/login', data)
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        assert 'token' in json_data
        TestUser.token = json_data['token']

    def test_token_profile_access(self, client: ClientWrapper):
        data = {
            'email': TestUser.NEW_USER['email'],
            'password': TestUser.NEW_USER['password']
        }

        resp = client.post('/login', data)
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        token = json_data['token']

        resp = client.get('/profile', token=token)
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        assert json_data['first_name'] == TestUser.NEW_USER['first_name']
        assert json_data['last_name'] == TestUser.NEW_USER['last_name']

        resp = client.get('/profile')
        assert resp.status_code == HTTPStatus.UNAUTHORIZED

    def test_client_token_profile_access(self, client: ClientWrapper):
        USER = user_customer_Customer
        client.login(user=USER)

        resp = client.get('/profile')
        assert resp.status_code == HTTPStatus.OK
        json_data = loads(resp.data.decode())
        assert json_data['first_name'] == USER['first_name']
        assert json_data['last_name'] == USER['last_name']

        client.logout()

        resp = client.get('/profile')
        assert resp.status_code == HTTPStatus.UNAUTHORIZED

    def test_profile_edit(self, client: ClientWrapper):
        data = {
            'first_name': 'Edited-first-name',
            'last_name': 'Edited-last-name'
        }

        resp = client.put('/profile', data, token=TestUser.token)
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/profile', token=TestUser.token)
        assert resp.status_code == HTTPStatus.OK
        profile = loads(resp.data.decode())
        assert profile['first_name'] == data['first_name']
        assert profile['last_name'] == data['last_name']
