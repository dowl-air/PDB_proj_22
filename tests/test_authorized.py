
from http import HTTPStatus
from json import loads

from helpers import ClientWrapper
from data import user_customer_Customer

# TODO only for JWT testing, remove later
def test_unauthorized(client: ClientWrapper):
	resp = client.get('/authorized')
	assert resp.status_code == HTTPStatus.UNAUTHORIZED

def test_authorized(client: ClientWrapper):
	USER = user_customer_Customer

	data = {
		'email': USER.email,
		'password': USER.last_name.lower()
	}

	resp = client.post('/login', data)
	assert resp.status_code == HTTPStatus.OK
	json_data = loads(resp.data.decode())
	assert json_data is not None

	token = json_data['token']

	resp = client.get('/authorized', token=token)
	assert resp.status_code == HTTPStatus.OK
	json_data = loads(resp.data.decode())
	assert json_data['message'] == 'You are authorized.'
	assert json_data['user_id'] == USER.id
	assert json_data['token_info'] is not None

def test_authorized_helper(client: ClientWrapper):
	client.login(user=user_customer_Customer)
	resp = client.get('/authorized')
	assert resp.status_code == HTTPStatus.OK
	assert resp.data.decode() is not None	
