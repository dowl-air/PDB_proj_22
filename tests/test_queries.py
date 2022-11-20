
from flask.testing import FlaskClient

def test_hello_world2(client: FlaskClient):
	resp = client.get('/')
	assert resp.status_code == 200
	assert 'Hello, World!' == resp.data.decode()
