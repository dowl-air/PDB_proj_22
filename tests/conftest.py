
import pytest

from app.create_app import create_app, db, mongo

from helpers import ClientWrapper
from data import (
	LOCATIONS, CATEGORIES, AUTHORS, BOOKS, BOOK_COPIES, USERS, BORROWALS, RESERVATIONS, REVIEWS,
	SQL_LOCATIONS, SQL_CATEGORIES, SQL_AUTHORS, SQL_BOOKS, SQL_BOOK_COPIES, SQL_USERS, SQL_BORROWALS, SQL_RESERVATIONS, SQL_REVIEWS
)

MONGO_DB_NAME = 'pdb'

@pytest.fixture(scope='session', autouse=True)
def clear_db() -> None:
	with create_app().app_context():
		db.drop_all()
		mongo.connection['default'].drop_database(MONGO_DB_NAME)

@pytest.fixture(scope='session', autouse=True)
def fill_db() -> None:
	with create_app().app_context():
		for arr in [LOCATIONS, CATEGORIES, AUTHORS, BOOKS, BOOK_COPIES, USERS, BORROWALS, RESERVATIONS, REVIEWS]:
			for it in arr:
				it.save()

		db.create_all()
		for arr in [SQL_LOCATIONS, SQL_CATEGORIES, SQL_AUTHORS, SQL_BOOKS, SQL_BOOK_COPIES, SQL_USERS, SQL_BORROWALS, SQL_RESERVATIONS, SQL_REVIEWS]:
			for it in arr:
				db.session.add(it)
			db.session.commit()

@pytest.fixture
def client() -> ClientWrapper:
	return ClientWrapper(create_app().test_client())
