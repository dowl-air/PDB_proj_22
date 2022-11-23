
from flask.testing import FlaskClient

from http import HTTPStatus
from json import loads

from helpers import (
	protected_put, post,
	assert_error_response
)

class TestUser:
	NEW_USER = {
		'id': 0,
		'first_name': 'First',
		'last_name': 'Last',
		'email': 'new_email@email.cz',
		'password': 'password123'
	}

	def test_register(self, client: FlaskClient):
		data = {
			'first_name': self.NEW_USER['first_name'],
			'last_name': self.NEW_USER['last_name'],
			'email': self.NEW_USER['email'],
			'password': self.NEW_USER['password']
		}

		resp = post('/register', data, client)
		assert resp.status_code == HTTPStatus.CREATED
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.NEW_USER['id'] = json_data['id']

	def test_register_invalid(self, client: FlaskClient):
		template = {
			'first_name': 'Invalid',
			'last_name': 'Registration',
			'email': 'another_email@email.cz',
			'password': '123password'
		}

		# missing email
		data = template.copy()
		data['email'] = None
		resp = post('/register', data, client)
		assert_error_response(resp)

		# duplicate email
		data = template.copy()
		data['email'] = self.NEW_USER['email']
		resp = post('/register', data, client)
		assert_error_response(resp)

		# missing password
		data = template.copy()
		data['password'] = None
		resp = post('/register', data, client)
		assert_error_response(resp)

	def test_login(self, client: FlaskClient):
		data = {
			'email': self.NEW_USER['email'],
			'password': self.NEW_USER['password']
		}

		resp = post('/login', data, client)
		assert resp.status_code == HTTPStatus.OK

	# TODO? JWT
	def test_logout(self, client: FlaskClient):
		resp = post('/logout', {}, client)
		assert resp.status_code == HTTPStatus.OK

	def test_profile_edit(self, client: FlaskClient):
		USER = {'id': self.NEW_USER['id']}

		data = {
			'first_name': 'Edited-first-name',
			'last_name': 'Edited-last-name'
		}

		resp = protected_put('/profile', data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/profile/%d' % USER['id']) # TODO
		assert resp.status_code == HTTPStatus.OK
		profile = loads(resp.data.decode())
		assert profile['first_name'] == data['first_name']
		assert profile['last_name'] == data['last_name']
