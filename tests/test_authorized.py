
import pytest

from http import HTTPStatus

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
	token = resp.data.decode()

	resp = client.get('/authorized', token=token)
	assert resp.status_code == HTTPStatus.OK
	assert resp.data.decode() is not None

def test_authorized_helper(client: ClientWrapper):
	client.login(user=user_customer_Customer)
	resp = client.get('/authorized')
	assert resp.status_code == HTTPStatus.OK
	assert resp.data.decode() is not None	
