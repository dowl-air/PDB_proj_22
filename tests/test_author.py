
from http import HTTPStatus
from json import loads

from helpers import (
    ClientWrapper,
    assert_error_response, assert_ok_created,
    find_by_id
)
from data import (
    author_Huxley,
    book_Brave_New_World,
    user_employee_Brno
)


class TestAuthor:
    new_id: int = 0

    def test_author_add(self, client: ClientWrapper):
        client.login(user_employee_Brno)

        data = {
            'first_name': 'Karel',
            'last_name': 'Čapek',
            'description': 'A czech 20th century novellist...'
        }

        resp = client.post('/authors', data)
        assert_ok_created(resp.status_code)
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        self.new_id = json_data['id']

        resp = client.get('/authors/%d' % self.new_id)
        assert resp.status_code == HTTPStatus.OK
        author = loads(resp.data.decode())
        assert data['first_name'] == author['first_name']
        assert data['last_name'] == author['last_name']
        assert data['description'] == author['description']

    def test_author_add_invalid(self, client: ClientWrapper):
        client.login(user_employee_Brno)

        data = {
            'first_name': 'Name',
            'description': 'Missing last name'
        }

        resp = client.post('/authors', data)
        assert_error_response(resp)

    def test_author_edit(self, client: ClientWrapper):
        client.login(user_employee_Brno)

        data = {
            'first_name': 'Edited author first name',
            'last_name': 'Edited author last name',
            'description': 'Edited author description'
        }
        assert self.new_id != 0

        resp = client.put('/authors/%d' % self.new_id, data)
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/authors/%d' % self.new_id)
        assert resp.status_code == HTTPStatus.OK
        author = loads(resp.data.decode())
        assert data['first_name'] == author['first_name']
        assert data['last_name'] == author['last_name']
        assert data['description'] == author['description']

    def test_author_edit_invalid(self, client: ClientWrapper):
        client.login(user_employee_Brno)

        data = {
            'first_name': None,
            'last_name': 'Last',
            'description': 'Invalid edit - no first name'
        }

        resp = client.put('/authors/%d' % self.new_id, data)
        assert_error_response(resp)

    def test_author_edit_propagation(self, client: ClientWrapper):
        client.login(user_employee_Brno)

        AUTHOR = author_Huxley
        BOOK = book_Brave_New_World

        data = {
            'first_name': 'Ray',
            'last_name': 'Bradbury',
            'description': 'Wrong author'
        }

        resp = client.put('/authors/%d' % AUTHOR.id, data)
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/books/%d' % BOOK.id)
        assert resp.status_code == HTTPStatus.OK
        book = loads(resp.data.decode())
        assert len(book['authors']) == 1
        author = book['authors'][0]
        assert author['first_name'] == data['first_name']
        assert author['last_name'] == data['last_name']

    def test_author_delete(self, client: ClientWrapper):
        client.login(user_employee_Brno)

        resp = client.delete('/authors/%d' % self.new_id, {})
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/authors/%d' % self.new_id)
        assert_error_response(resp)

    def test_author_delete_propagation(self, client: ClientWrapper):
        client.login(user_employee_Brno)

        BOOK = book_Brave_New_World
        AUTHOR = author_Huxley

        resp = client.get('/books/%d' % BOOK.id)
        assert resp.status_code == HTTPStatus.OK
        book = loads(resp.data.decode())
        assert find_by_id(AUTHOR.id, book['authors']) is not None

        resp = client.delete('/authors/%d' % AUTHOR.id, {})
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/books/%d' % BOOK.id)
        assert resp.status_code == HTTPStatus.OK
        book = loads(resp.data.decode())
        assert len(book['authors']) == 0
