
from flask.testing import FlaskClient
from werkzeug.test import TestResponse
from deepdiff.diff import DeepDiff

from http import HTTPStatus
from json import loads
from bson import json_util

from typing import Optional

def serialize(arg) -> str:
	if isinstance(arg, list):
		return json_util.dumps([x.to_mongo() for x in arg])

	return arg.to_json()

def entity_compare(data, entity) -> None:
	assert loads(data.decode()) == loads(serialize(entity))

def check_error_message(data) -> None:
	assert data.decode() is not None

def expect_error(resp: TestResponse) -> None:
	assert resp.status_code not in [HTTPStatus.OK, HTTPStatus.NOT_FOUND]
	assert resp.data.decode() is not None

def assert_error_response(resp: TestResponse) -> None:
	assert resp.status_code not in [HTTPStatus.OK, HTTPStatus.NOT_FOUND, HTTPStatus.UNAUTHORIZED]
	assert resp.data.decode() is not None

def login(client: FlaskClient, email: str, password: str) -> None:
	resp = client.post('/login', data={'email': email, 'password': password})
	assert resp.status_code == HTTPStatus.OK

def logout(client: FlaskClient) -> None:
	resp = client.post('/logout')
	assert resp.status_code == HTTPStatus.OK

def assert_dict_equal(actual, expected, ignore_list=['dictionary_item_removed', 'iterable_item_removed']) -> None:
	diff = DeepDiff(actual, expected)
	diff_keys = list(diff.keys())
	if diff_keys:
		diff_keys = list(filter(lambda x: x not in ignore_list, diff_keys))
		if len(diff_keys) == 0:
			return

	assert actual == expected

def protected_post(endpoint: str, data: dict, client: FlaskClient, user) -> TestResponse:
	data['authorization'] = {
		'user_id': user['id']
	}

	return client.post(endpoint, data=data)

def protected_delete(endpoint: str, client: FlaskClient, user, data: Optional[dict] = None) -> TestResponse:
	if data is None:
		data = {}

	data['authorization'] = {
		'user_id': user['id']
	}

	return client.delete(endpoint, data=data)

def protected_put(endpoint: str, data: dict, client: FlaskClient, user) -> TestResponse:
	data['authorization'] = {
		'user_id': user['id']
	}

	return client.put(endpoint, data=data)

