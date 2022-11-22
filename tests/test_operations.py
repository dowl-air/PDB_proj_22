
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
	BOOK_COPY_STATE_GOOD, BOOK_COPY_STATE_DAMAGED,
	authorOrwell, authorHuxley, authorTolkien,
	book1984, bookBraveNewWorld, bookAnimalFarm,
	locationBrno, locationOlomouc,
	categoryFable, categoryHistory, categoryNonFiction, categoryFantasy,
	bc1984Brno1, bc1984London1, bc1984London2,
	userEmployeeBrno, userAdmin
)

class TestCategory:
	new_id: int

	def test_category_add(self, client: FlaskClient):
		data = {
			'name': 'Novel',
			'description': 'A novel is a relatively long work of narrative fiction, typically...'
		}

		USER = userEmployeeBrno

		resp = protected_post('/category/add', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/category/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		category = loads(resp.data.decode())
		assert data['name'] == category['name']
		assert data['description'] == category['description']

	def test_category_add_invalid(self, client: FlaskClient):
		data = {
			'description': 'Missing category name'
		}

		USER = userEmployeeBrno

		resp = protected_post('/category/add', data, client, USER)
		assert_error_response(resp)

	def test_category_edit(self, client: FlaskClient):
		data = {
			'name': 'Edited category name',
			'description': 'Edited category description'
		}

		USER = userEmployeeBrno

		resp = protected_put('/category/%d/edit' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/category/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		category = loads(resp.data.decode())
		assert data['name'] == category['name']
		assert data['description'] == category['description']

	def test_category_edit_invalid(self, client: FlaskClient):
		data = {
			'name': None,
			'description': 'Invalid edit - no name'
		}

		USER = userEmployeeBrno

		resp = protected_put('/category/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_category_edit_propagation(self, client: FlaskClient):
		data = {
			'name': 'Fairy tale',
			'description': 'Fantastical story'
		}

		USER = userEmployeeBrno

		resp = protected_put('/category/%d/edit' % categoryFable.id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % bookAnimalFarm.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		assert_dict_equal(book['categories'], [data])
	
	def test_category_delete(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_delete('/category/%d/delete' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/category/%d' % self.new_id)
		assert_error_response(resp)

	def test_category_delete_propagation(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_delete('/category/%d/delete' % categoryFable.id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % bookAnimalFarm.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		assert len(book['categories']) == 1
		assert book['categories'][0]['id'] != categoryFable.id
		
class TestLocation:
	new_id: int

	def test_location_add(self, client: FlaskClient):
		data = {
			'name': 'VUT FIT',
			'address': 'Božetěchova 1/2, 612 00 Brno-Královo Pole'
		}

		USER = userAdmin

		resp = protected_post('/location/add', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/location/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		location = loads(resp.data.decode())
		assert data['name'] == location['name']
		assert data['address'] == location['address']

	def test_location_add_invalid(self, client: FlaskClient):
		data = {
			'address': 'Missing location name'
		}

		USER = userAdmin

		resp = protected_post('/location/add', data, client, USER)
		assert_error_response(resp)

	def test_location_edit(self, client: FlaskClient):
		data = {
			'name': 'Edited VUT FIT location',
			'address': 'Edited location address'
		}

		USER = userAdmin

		resp = protected_put('/location/%d/edit' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/location/%d' % id)
		assert resp.status_code == HTTPStatus.OK
		location = loads(resp.data.decode())
		assert data['name'] == location['name']
		assert data['address'] == location['address']

	def test_location_edit_invalid(self, client: FlaskClient):
		data = {
			'name': None,
			'description': 'Invalid edit - no name'
		}

		USER = userAdmin

		resp = protected_put('/location/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_location_edit_propagation(self, client: FlaskClient):
		data = {
			'name': 'Ostrava',
			'address': 'idk'
		}

		USER = userAdmin

		resp = protected_put('/location/%d/edit' % locationBrno.id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book_copy/%d' % bc1984Brno1.id)
		assert resp.status_code == HTTPStatus.OK
		book_copy = loads(resp.data.decode())
		assert book_copy['location']['name'] == data['name']
		assert book_copy['location']['address'] == data['address']
	
	def test_location_delete(self, client: FlaskClient):
		USER = userAdmin

		resp = protected_delete('/location/%d/delete' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/location/%d' % self.new_id)
		assert_error_response(resp)

	# cannot delete location with assigned book copies
	def test_location_delete_invalid(self, client: FlaskClient):
		USER = userAdmin

		resp = protected_delete('/location/%d/delete' % locationBrno.id, client, USER)
		assert_error_response(resp)

class TestAuthor:
	new_id: int

	def test_author_add(self, client: FlaskClient):
		data = {
			'first_name': 'Karel',
			'last_name': 'Čapek',
			'description': 'A czech 20th century novellist...'
		}

		USER = userEmployeeBrno

		resp = protected_post('/author/add', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/author/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		author = loads(resp.data.decode())
		assert data['first_name'] == author['first_name']
		assert data['last_name'] == author['last_name']
		assert data['description'] == author['description']

	def test_author_add_invalid(self, client: FlaskClient):
		data = {
			'first_name': 'Name',
			'description': 'Missing last name'
		}

		USER = userEmployeeBrno

		resp = protected_post('/author/add', data, client, USER)
		assert_error_response(resp)

	def test_author_edit(self, client: FlaskClient):
		data = {
			'first_name': 'Edited author first name',
			'last_name': 'Edited author last name',
			'description': 'Edited author description'
		}

		USER = userEmployeeBrno

		resp = protected_put('/author/%d/edit' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/author/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		author = loads(resp.data.decode())
		assert data['first_name'] == author['first_name']
		assert data['last_name'] == author['last_name']
		assert data['description'] == author['description']

	def test_author_edit_invalid(self, client: FlaskClient):
		data = {
			'first_name': None,
			'last_name': 'Last',
			'description': 'Invalid edit - no first name'
		}

		USER = userEmployeeBrno

		resp = protected_put('/author/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_author_edit_propagation(self, client: FlaskClient):
		data = {
			'first_name': 'Ray',
			'last_name': 'Bradbury',
			'description': 'Wrong author'
		}

		USER = userEmployeeBrno

		resp = protected_put('/author/%d/edit' % authorHuxley.id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % bookBraveNewWorld)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		assert len(book['authors']) == 1
		author = book['authors'][0]
		assert author['first_name'] == data['first_name']
		assert author['last_name'] == data['last_name']
	
	def test_author_delete(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_delete('/author/%d/delete' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/author/%d' % self.new_id)
		assert_error_response(resp)

	def test_author_delete_propagation(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_delete('/author/%d/delete' % authorHuxley.id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % bookBraveNewWorld.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		assert len(book['authors']) == 0

class TestBookCopy:
	new_id: int

	def test_book_copy_add(self, client: FlaskClient):
		LOCATION = locationBrno

		data = {
			'book_id': book1984.id,
			'location_id': LOCATION.id,
			'print_date': date(2019, 10, 5),
			'note': 'Note',
			'state': BOOK_COPY_STATE_GOOD
		}

		USER = userEmployeeBrno

		resp = protected_post('/book_copy/add', data, client, USER)
		assert resp.status_code == HTTPStatus.OK
		json_data = loads(resp.data.decode())
		assert 'id' in json_data

		self.new_id = json_data['id']

		resp = client.get('/book_copy/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		copy = loads(resp.data.decode())
		assert copy['book_id'] == data['book_id']
		assert copy['print_date'] == data['print_date']
		assert copy['note'] == data['note']
		assert copy['state'] == data['state']
		location = copy['location']
		assert location['id'] == LOCATION.id
		assert location['name'] == LOCATION.name
		assert location['address'] == LOCATION.address

	def test_book_copy_add_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK = book1984
		LOCATION = locationBrno

		template = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': date(2019, 10, 5),
			'note': 'Note',
			'state': BOOK_COPY_STATE_GOOD
		}

		# missing book id
		data = template.copy()
		data['book_id'] = None
		resp = protected_post('/book_copy/add', data, client, USER)
		assert_error_response(resp)

		# missing location id
		data = template.copy()
		data['location_id'] = None
		resp = protected_post('/book_copy/add', data, client, USER)
		assert_error_response(resp)

		# missing print date
		data = template.copy()
		data['print_date'] = None
		resp = protected_post('/book_copy/add', data, client, USER)
		assert_error_response(resp)

	def test_book_copy_edit(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK = bookAnimalFarm
		LOCATION = locationOlomouc

		data = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': date(2018, 7, 20),
			'note': 'Edited note',
			'state': BOOK_COPY_STATE_DAMAGED
		}

		resp = protected_put('/book_copy/%d/edit' % self.new_id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book_copy/%d' % self.new_id)
		assert resp.status_code == HTTPStatus.OK
		copy = loads(resp.data.decode())
		assert data['book_id'] == copy['book_id']
		assert data['print_date'] == copy['print_date']
		assert data['note'] == copy['note']
		assert data['state'] == copy['state']
		location = copy['location']
		assert location['id'] == LOCATION.id
		assert location['name'] == LOCATION.name
		assert location['address'] == LOCATION.address

	def test_book_copy_edit_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK = book1984
		LOCATION = locationBrno

		template = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': date(2019, 10, 5),
			'note': 'Note',
			'state': BOOK_COPY_STATE_GOOD
		}

		# missing book id
		data = template.copy()
		data['book_id'] = None
		resp = protected_post('/book_copy/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

		# missing location id
		data = template.copy()
		data['location_id'] = None
		resp = protected_post('/book_copy/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

		# missing print date
		data = template.copy()
		data['print_date'] = None
		resp = protected_post('/book_copy/%d/edit' % self.new_id, data, client, USER)
		assert_error_response(resp)

	def test_book_copy_edit_propagation(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK_COPY = bc1984Brno1
		BOOK = bookAnimalFarm
		LOCATION = locationOlomouc

		data = {
			'book_id': BOOK.id,
			'location_id': LOCATION.id,
			'print_date': date(2017, 4, 16),
			'note': 'Edited note',
			'state': BOOK_COPY_STATE_DAMAGED
		}

		resp = protected_put('/book_copy/%d/edit' % BOOK_COPY.id, data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		copies = book['book_copies']
		copies = list(filter(lambda x: x['id'] == BOOK_COPY.id, copies))
		assert len(copies) == 1
		copy = copies[0]
		assert copy['print_date'] == data['print_date']
		assert copy['note'] == data['note']
		assert copy['state'] == data['state']
		assert copy['location_id'] == LOCATION.id
	
	def test_book_copy_delete(self, client: FlaskClient):
		USER = userEmployeeBrno

		resp = protected_delete('/book_copy/%d/delete' % self.new_id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book_copy/%d' % self.new_id)
		assert_error_response(resp)

	# cannot delete book copy with borrowals
	def test_book_copy_delete_invalid(self, client: FlaskClient):
		USER = userEmployeeBrno
		BOOK_COPY = bc1984London1

		resp = protected_delete('/book_copy/%d/delete' % BOOK_COPY.id, client, USER)
		assert_error_response(resp)

	def test_book_copy_delete_propagation(self, client: FlaskClient):
		USER = userEmployeeBrno

		BOOK_COPY = bc1984London2
		BOOK = book1984

		resp = protected_delete('/book_copy/%d/delete' % BOOK_COPY.id, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/book/%d' % BOOK.id)
		assert resp.status_code == HTTPStatus.OK
		book = loads(resp.data.decode())
		copies = list(filter(lambda x: x['id'] == BOOK_COPY.id, copies))
		assert len(copies) == 0

class TestBook:
	new_id: int
	new_book_author_id: int

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

class TestUser:
	NEW_USER = {
		'first_name': 'First',
		'last_name': 'Last',
		'email': 'new_email@email.cz',
		'password': 'password123'
	}

	def test_register(self, client: FlaskClient):
		resp = client.post('/register', data=self.NEW_USER)
		assert resp.status_code == HTTPStatus.OK
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
		resp = client.post('/register', data=data)
		assert_error_response(resp)

		# duplicate email
		data = template.copy()
		data['email'] = self.NEW_USER['email']
		resp = client.post('/register', data=data)
		assert_error_response(resp)

		# missing password
		data = template.copy()
		data['password'] = None
		resp = client.post('/register', data=data)
		assert_error_response(resp)

	def test_login(self, client: FlaskClient):
		data = {
			'email': self.NEW_USER['email'],
			'password': self.NEW_USER['password']
		}

		resp = client.post('/login', data=data)
		assert resp.status_code == HTTPStatus.OK

	# TODO? JWT
	def test_logout(self, client: FlaskClient):
		resp = client.post('/logout')
		assert resp.status_code == HTTPStatus.OK

	def test_profile_edit(self, client: FlaskClient):
		USER = {'id': self.NEW_USER['id']}

		data = {
			'first_name': 'Edited-first-name',
			'last_name': 'Edited-last-name'
		}

		resp = protected_put('/profile/edit', data, client, USER)
		assert resp.status_code == HTTPStatus.OK

		resp = client.get('/profile/%d' % USER['id'])
		assert resp.status_code == HTTPStatus.OK
		profile = loads(resp.data.decode())
		assert profile['first_name'] == data['first_name']
		assert profile['last_name'] == data['last_name']
