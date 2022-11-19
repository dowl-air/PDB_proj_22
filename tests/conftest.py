
import pytest
from app.create_app import create_app, db, mongo

@pytest.fixture(scope='session', autouse=True)
def clear_db():
	with create_app().app_context():
		db.drop_all()
		mongo.connection['default'].drop_database('pdb')

@pytest.fixture
def client():
	with create_app().test_client() as client:
		yield client
