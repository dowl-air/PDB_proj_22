
import pytest

from app.create_app import create_app

from helpers import ClientWrapper
from data import clear_db, fill_db


# removes data from both databases and refills them with test data
@pytest.fixture(scope='session', autouse=True)
def init_db() -> None:
	clear_db()
	fill_db()

# test client to send requests to endpoint
@pytest.fixture
def client() -> ClientWrapper:
	return ClientWrapper(create_app({'producer_log': False}).test_client())
