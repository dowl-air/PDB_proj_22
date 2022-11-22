
from flask.testing import FlaskClient

from datetime import date
from http import HTTPStatus
from json import loads

from helpers import (
	assert_dict_equal, assert_error_response,
	find_by_id,
	protected_post, protected_put, protected_delete
)
from conftest import (
	authorOrwell, authorHuxley, authorTolkien,
	book1984, bookAnimalFarm,
	categoryFable, categoryHistory, categoryNonFiction, categoryFantasy,
	userEmployeeBrno,
)

class TestBook:
	new_id: int = 0
	new_book_author_id: int = 0

	def test_book_add(self, client: FlaskClient):
		USER = userEmployeeBrno

		AUTHOR = authorOrwell
		CATEGORY1 = categoryHistory
		CATEGORY2 = categoryNonFiction

		data = {
			'name': 'Homage to Catalonia',
			'ISBN': '978-0-00-844274-3',
			'release_date': date(1938, 4, 25),
			'description': 'In 1936 Orwell went to Spain to report on the Civil War...',
			'authors': [AUTHOR.id],
			'categories': [CATEGORY1.id, CATEGORY2.id]
		}

		resp = protected_post('/book/add', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']
		self.new_book_author_id = AUTHOR.id

		resp = client.get('/book/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		assert book['name'] == data['name']
		assert book['ISBN'] == data['ISBN']
		assert book['release_date'] == data['release_date']
		assert book['description'] == data['description']
		assert len(book['authors']) == 1
		author = book['authors'][0]
		assert author['id'] == AUTHOR.id
		assert author['first_name'] == AUTHOR.first_name
		assert author['last_name'] == AUTHOR.last_name
		assert len(book['categories']) == 2
		assert_dict_equal(book['categories'], [
			{'id': CATEGORY1.id, 'name': CATEGORY1.name, 'description': CATEGORY1.description},
			{'id': CATEGORY2.id, 'name': CATEGORY2.name, 'description': CATEGORY2.description}
		])

		resp = client.get('/author/%d' % AUTHOR.id)
		assert resp.status_code == HTTPStatus.OK
		author = loads(resp.data.decode())
		book = find_by_id(self.new_id)
		assert book is not None
		assert book['name'] == data['name']
		assert book['ISBN'] == data['ISBN']
		assert book['release_date'] == data['release_date']
		assert book['description'] == data['description']

	def test_book_add_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno

		AUTHOR = authorTolkien
		CATEGORY = categoryFantasy

		template = {
			'name': 'The Fellowship of the Ring',
			'ISBN': '978-0345339706',
			'release_date': date(1954, 7, 29),
			'description': 'The Fellowship of the Ring is the first of three...',
			'authors': [AUTHOR.id],
			'categories': [CATEGORY.id]
		}

		# missing name
		data = template.copy()
		data['name'] = None
		resp = protected_post('/book/add', data, client, USER)
		assert_error_response(resp)

		# missing ISBN
		data = template.copy()
		data['ISBN'] = None
		resp = protected_post('/book/add', data, client, USER)
		assert_error_response(resp)

		# duplicate ISBN
		data = template.copy()
		data['ISBN'] = book1984.ISBN
		resp = protected_post('/book/add', data, client, USER)
		assert_error_response(resp)

		# unknown author
		data = template.copy()
		data['authors'] = [300]
		resp = protected_post('/book/add', data, client, USER)
		assert_error_response(resp)

		# unknown category
		data = template.copy()
		data['categories'] = [300]
		resp = protected_post('/book/add', data, client, USER)
		assert_error_response(resp)

	def test_book_edit(self, client: FlaskClient):
		USER = userEmployeeBrno

		AUTHOR = authorHuxley
		CATEGORY = categoryFable

		data = {
			'name': 'Edited name',
			'ISBN': 'Edited ISBN',
			'release_date': date(1900, 1, 1),
			'description': 'Edited description',
			'authors': [AUTHOR.id],
			'categories': [CATEGORY.id]
		}

		resp = protected_put('/book/%d/edit' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		self.new_book_author_id = AUTHOR.id

		resp = client.get('/book/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		assert data['name'] == book['name']
		assert data['ISBN'] == book['ISBN']
		assert data['release_date'] == book['release_date']
		assert data['description'] == book['description']
		assert len(book['authors']) == 1
		author = book['authors'][0]
		assert author['id'] == AUTHOR.id
		assert author['first_name'] == AUTHOR.first_name
		assert author['last_name'] == AUTHOR.last_name
		assert len(book['categories']) == 1
		category = book['categories'][0]
		assert category['id'] == CATEGORY.id
		assert category['name'] == CATEGORY.name
		assert category['description'] == CATEGORY.description

	def test_book_edit_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno

		AUTHOR = authorTolkien
		CATEGORY = categoryFantasy

		template = {
			'name': 'Edited name',
			'ISBN': 'Edited ISBN (invalid edit test)',
			'release_date': date(1950, 2, 2),
			'description': 'Edited description',
			'authors': [AUTHOR.id],
			'categories': [CATEGORY.id]
		}

		# missing name
		data = template.copy()
		data['name'] = None
		resp = protected_post('/book/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

		# missing ISBN
		data = template.copy()
		data['ISBN'] = None
		resp = protected_post('/book/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

		# duplicate ISBN
		data = template.copy()
		data['ISBN'] = book1984.ISBN
		resp = protected_post('/book/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

		# unknown author
		data = template.copy()
		data['authors'] = [300]
		resp = protected_post('/book/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

		# unknown category
		data = template.copy()
		data['categories'] = [300]
		resp = protected_post('/book/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_book_edit_propagation(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK = bookAnimalFarm
		ORIGINAL_AUTHOR_ID = bookAnimalFarm.authors[0]['id']
		NEW_AUTHOR = authorHuxley

		data = {
			'name': 'Animal Farm (edited)',
			'ISBN': 'Animal Farm ISBN (edited)',
			'release_date': date(1947, 7, 7),
			'description': 'Animal Farm description (edited)',
			'authors': [NEW_AUTHOR.id],
			'categories': []
		}

		resp = protected_put('/book/%d/edit' % BOOK.id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/author/%d' % ORIGINAL_AUTHOR_ID)
		assert resp.status_code == HTTPStatus.OK
		author = loads(resp.data.decode())
		assert find_by_id(BOOK.id, author['books']) is None

		resp = client.get('/author/%d' % NEW_AUTHOR.id)
		assert resp.status_code == HTTPStatus.OK
		author = loads(resp.data.decode())
		book = find_by_id(BOOK.id, author['books'])
		assert book['name'] == data['name']
		assert book['ISBN'] == data['ISBN']
		assert book['release_date'] == data['release_date']
		assert book['description'] == data['description']

	def test_book_delete(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_delete('/book/%d/delete' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % self.new_id)
		assert_error_response(resp)

		# delete propagation
		resp = client.get('/author/%d' % self.new_book_author_id)
		assert resp.status_code == HTTPStatus.OK
		author = loads(resp.data.decode())
		assert find_by_id(self.new_id, author['books']) is None

	# cannot delete book with copies
	def test_book_delete_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK = book1984

		resp = protected_delete('/book/%d/delete' % BOOK.id, client, USER)
		assert_error_response(resp)
