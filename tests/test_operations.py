
from flask.testing import FlaskClient

from datetime import date
from http import HTTPStatus
from json import loads

from helpers import (
	login, expect_error, entity_compare, assert_dict_equal, assert_error_response,
	protected_post, protected_put, protected_delete	
)
from conftest import (
	embed_author_list,

	BOOK_COPY_STATE_GOOD, BOOK_COPY_STATE_DAMAGED,

	authorOrwell, authorHuxley, authorTolkien,
	book1984, bookBraveNewWorld, bookAnimalFarm,
	locationBrno, locationOlomouc,
	categoryFable,
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
		resp = protected_post('/book_copy/%d/edit', data, client, USER)
		assert_error_response(resp)

		# missing location id
		data = template.copy()
		data['location_id'] = None
		resp = protected_post('/book_copy/%d/edit', data, client, USER)
		assert_error_response(resp)

		# missing print date
		data = template.copy()
		data['print_date'] = None
		resp = protected_post('/book_copy/%d/edit', data, client, USER)
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

NEW_USER_EMAIL = 'new_email@email.cz'

def test_register(client: FlaskClient):
	data = {
		'first_name': 'First',
		'last_name': 'Last',
		'email': NEW_USER_EMAIL,
		'password': 'password123'
	}

	resp = client.post('/register', data=data)
	assert resp.status_code == HTTPStatus.OK

	login(client, email=data['email'], password=data['password'])

def test_register_invalid(client: FlaskClient):
	data = {
		'first_name': 'X',
		'password': '123password'
	}

	resp = client.post('/register', data=data)
	expect_error(resp)

def test_register_duplicate_email(client: FlaskClient):
	data = {
		'first_name': 'Different',
		'last_name': 'Name',
		'email': NEW_USER_EMAIL,
		'password': 'abcdefg123'
	}

	resp = client.post('/register', data=data)
	expect_error(resp)

HOMAGE_TO_CATALONIA_DATA = {
	'name': 'Homage to Catalonia',
	'ISBN': '978-0-00-844274-3',
	'release_date': date(1938, 4, 25),
	'description': "In 1936 Orwell went to Spain to report on the Civil War...",
	'authors': [authorOrwell.id]
}

def test_add_book(client: FlaskClient):
	resp = client.post('/book/add', data=HOMAGE_TO_CATALONIA_DATA)
	assert resp.status_code == HTTPStatus.OK
	json_data = loads(resp.data.decode())
	assert 'id' in json_data

	HOMAGE_TO_CATALONIA_DATA['id'] = json_data['id']

	resp = client.get('/book/%d' % json_data['id'])
	assert resp.status_code == HTTPStatus.OK
	json_data = loads(resp.data.decode())
	assert json_data['name'] == HOMAGE_TO_CATALONIA_DATA['name']

	resp = client.get('/author/%d' % authorOrwell.id)
	assert resp.status_code == HTTPStatus.OK
	author = loads(resp.data.decode())
	assert len(author['books']) == 3
	assert len(filter(lambda x: x == HOMAGE_TO_CATALONIA_DATA['name'], author['books'])) == 1

def test_add_book_invalid(client: FlaskClient):
	data = {
		'release_date': date(1950, 11, 11),
		'description': 'text'
	}

	resp = client.post('/book/add', data=data)
	expect_error(resp)

def test_add_book_invalid_unknown_author(client: FlaskClient):
	data = {
		'name': 'The Stranger',
		'ISBN': '978-0679720201',
		'release_date': date(1942, 1, 1),
		'description': "In 1936 Orwell went to Spain to report on the Civil War...",
		'authors': [300]
	}

	resp = client.post('/book/add', data=data)
	expect_error(resp)

def test_update_book(client: FlaskClient):
	NEW_NAME = 'New name'
	NEW_DESCRIPTION = 'New description'
	NEW_AUTHORS = [authorHuxley.id, authorTolkien.id]
	data = {
		'id': book1984.id,
		'name': NEW_NAME,
		'ISBN': book1984.ISBN,
		'release_date': book1984.release_date,
		'description': NEW_DESCRIPTION,
		'authors': NEW_AUTHORS
	}

	resp = client.post('/book/%d/edit' % book1984.id, data=data)
	assert resp.status_code == HTTPStatus.OK

	edited_book = book1984
	edited_book.name = NEW_NAME
	edited_book.description = NEW_DESCRIPTION
	edited_book.authors = embed_author_list([authorHuxley, authorTolkien])

	resp = client.get('/book/%d' % book1984.id)
	assert resp.status_code == HTTPStatus.OK
	entity_compare(resp.data, edited_book)

	resp = client.get('/author/%d' % authorHuxley.id)
	assert resp.status_code == HTTPStatus.OK
	author = loads(resp.data.decode())
	assert len(author['books']) == 2
	assert len(filter(lambda x: x == NEW_NAME, author['books'])) == 1

	book1984.save() # TODO

def test_delete_book(client: FlaskClient):
	resp = client.get('/book/%d' % HOMAGE_TO_CATALONIA_DATA['id'])
	assert resp.status_code == HTTPStatus.OK

	resp = client.delete('/book/%d/delete' % HOMAGE_TO_CATALONIA_DATA['id'])
	assert resp.status_code == HTTPStatus.OK

	resp = client.get('/book/%d')
	expect_error(resp)

	resp = client.get('/author/%d' % authorOrwell.id)
	assert resp.status_code == HTTPStatus.OK
	author = loads(resp.data.decode())
	assert len(author['books']) == 2
	assert len(filter(lambda x: x == HOMAGE_TO_CATALONIA_DATA['name'], author['books'])) == 0

def test_delete_book_invalid_existing_copies(client: FlaskClient):
	resp = client.delete('/book/%d/delete' % bookBraveNewWorld.id)
	expect_error(resp)

def test_add_book_copy(client: FlaskClient):
	data = {
		'book_id': book1984.id,
		'location_id': locationBrno.id,
		'print_date': date(2021, 10, 10),
		'note': 'Newly added'
	}

	resp = client.post('/book_copy/add')
	assert resp.status_code == HTTPStatus.OK
	json_data = loads(resp.data.decode())
	assert 'id' in json_data

	HOMAGE_TO_CATALONIA_DATA['id'] = json_data['id']

	resp = client.get('/author/%d' % authorOrwell.id)
	assert resp.status_code == HTTPStatus.OK
	author = loads(resp.data.decode())
	assert len(author['books']) == 3
	assert len(filter(lambda x: x == HOMAGE_TO_CATALONIA_DATA['name'], author['books'])) == 1
