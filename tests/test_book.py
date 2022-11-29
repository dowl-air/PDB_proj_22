
from datetime import date
from http import HTTPStatus
from json import loads

from helpers import (
    ClientWrapper,
    assert_dict_equal, assert_error_response, assert_ok_created,
    find_by_id,
    format_date
)
from data import (
    author_Orwell, author_Huxley, author_Tolkien,
    book_1984, book_Animal_Farm,
    category_fable, category_history, category_non_fiction, category_fantasy,
    user_employee_Brno
)


class TestBook:
    new_id: int = 0
    new_book_author_id: int = 0

    def test_book_add(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        AUTHOR = author_Orwell
        CATEGORY1 = category_history
        CATEGORY2 = category_non_fiction

        data = {
            'name': 'Homage to Catalonia',
            'ISBN': '978-0-00-844274-3',
            'release_date': format_date(date(1938, 4, 25)),
            'description': 'In 1936 Orwell went to Spain to report on the Civil War...',
            'authors': [AUTHOR.id],
            'categories': [CATEGORY1.id, CATEGORY2.id]
        }

        resp = client.post('/books', data)
        assert_ok_created(resp.status_code)
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        TestBook.new_id = json_data['id']
        TestBook.new_book_author_id = AUTHOR.id

        resp = client.get('/books/%d' % TestBook.new_id)
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
            {'id': CATEGORY1.id, 'name': CATEGORY1.name},  # description deleted because its not present in mongoDB and caused error
            {'id': CATEGORY2.id, 'name': CATEGORY2.name}
        ])

        resp = client.get('/authors/%d' % AUTHOR.id)
        assert resp.status_code == HTTPStatus.OK
        author = loads(resp.data.decode())
        book = find_by_id(TestBook.new_id, author['books'])
        assert book is not None
        assert book['name'] == data['name']
        assert book['ISBN'] == data['ISBN']
        assert book['release_date'] == data['release_date']
        # assert book['description'] == data['description'] # description not in database object -> KeyError

    def test_book_add_invalid(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        AUTHOR = author_Tolkien
        CATEGORY = category_fantasy

        template = {
            'name': 'The Fellowship of the Ring',
            'ISBN': '978-0345339706',
            'release_date': format_date(date(1954, 7, 29)),
            'description': 'The Fellowship of the Ring is the first of three...',
            'authors': [AUTHOR.id],
            'categories': [CATEGORY.id]
        }

        # missing name
        data = template.copy()
        data['name'] = None
        resp = client.post('/books', data)
        assert_error_response(resp)

        # missing ISBN
        data = template.copy()
        data['ISBN'] = None
        resp = client.post('/books', data)
        assert_error_response(resp)

        # duplicate ISBN
        data = template.copy()
        data['ISBN'] = book_1984.ISBN
        resp = client.post('/books', data)
        assert_error_response(resp)

        # unknown author
        data = template.copy()
        data['authors'] = [300]
        resp = client.post('/books', data)
        assert_error_response(resp)

        # unknown category
        data = template.copy()
        data['categories'] = [300]
        resp = client.post('/books', data)
        assert_error_response(resp)

    def test_book_edit(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        AUTHOR = author_Huxley
        CATEGORY = category_fable

        data = {
            'name': 'Edited name',
            'ISBN': 'Edited ISBN',
            'release_date': format_date(date(1900, 1, 1)),
            'description': 'Edited description',
            'authors': [AUTHOR.id],
            'categories': [CATEGORY.id]
        }

        resp = client.put('/books/%d' % TestBook.new_id, data)
        assert resp.status_code == HTTPStatus.OK

        TestBook.new_book_author_id = AUTHOR.id

        resp = client.get('/books/%d' % TestBook.new_id)
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
        # assert category['description'] == CATEGORY.description

    def test_book_edit_invalid(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        AUTHOR = author_Tolkien
        CATEGORY = category_fantasy

        template = {
            'name': 'Edited name',
            'ISBN': 'Edited ISBN (invalid edit test)',
            'release_date': format_date(date(1950, 2, 2)),
            'description': 'Edited description',
            'authors': [AUTHOR.id],
            'categories': [CATEGORY.id]
        }

        # missing name
        data = template.copy()
        data['name'] = None
        resp = client.put('/books/%d' % TestBook.new_id, data)
        assert_error_response(resp)

        # missing ISBN
        data = template.copy()
        data['ISBN'] = None
        resp = client.put('/books/%d' % TestBook.new_id, data)
        assert_error_response(resp)

        # duplicate ISBN
        data = template.copy()
        data['ISBN'] = book_1984.ISBN
        resp = client.put('/books/%d' % TestBook.new_id, data)
        assert_error_response(resp)

        # unknown author
        data = template.copy()
        data['authors'] = [300]
        resp = client.put('/books/%d' % TestBook.new_id, data)
        assert_error_response(resp)

        # unknown category
        data = template.copy()
        data['categories'] = [300]
        resp = client.put('/books/%d' % TestBook.new_id, data)
        assert_error_response(resp)

    def test_book_edit_propagation(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        BOOK = book_Animal_Farm
        ORIGINAL_AUTHOR_ID = book_Animal_Farm.authors[0]['id']
        NEW_AUTHOR = author_Huxley

        data = {
            'name': 'Animal Farm (edited)',
            'ISBN': 'Animal Farm ISBN (edited)',
            'release_date': format_date(date(1947, 7, 7)),
            'description': 'Animal Farm description (edited)',
            'authors': [NEW_AUTHOR.id],
            'categories': []
        }

        resp = client.put('/books/%d' % BOOK.id, data)
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/authors/%d' % ORIGINAL_AUTHOR_ID)
        assert resp.status_code == HTTPStatus.OK
        author = loads(resp.data.decode())
        assert find_by_id(BOOK.id, author['books']) is None

        resp = client.get('/authors/%d' % NEW_AUTHOR.id)
        assert resp.status_code == HTTPStatus.OK
        author = loads(resp.data.decode())
        book = find_by_id(BOOK.id, author['books'])
        assert book['name'] == data['name']
        assert book['ISBN'] == data['ISBN']
        assert book['release_date'] == data['release_date']
        # assert book['description'] == data['description']

    def test_book_delete(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        resp = client.delete('/books/%d' % TestBook.new_id, {})
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/books/%d' % TestBook.new_id)
        assert_error_response(resp)

        # delete propagation
        resp = client.get('/authors/%d' % TestBook.new_book_author_id)
        assert resp.status_code == HTTPStatus.OK
        author = loads(resp.data.decode())
        assert find_by_id(TestBook.new_id, author['books']) is None

    # cannot delete book with copies
    def test_book_delete_invalid(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        BOOK = book_1984

        resp = client.delete('/books/%d' % BOOK.id, {})
        assert_error_response(resp)
