
from http import HTTPStatus
from json import loads

from helpers import (
    ClientWrapper,
    assert_error_response, assert_ok_created,
    find_by_id
)
from data import (
    book_Animal_Farm,
    category_fable,
    user_employee_Brno
)


class TestCategory:
    new_id: int = 0

    def test_category_add(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        data = {
            'name': 'Novel',
            'description': 'A novel is a relatively long work of narrative fiction, typically...'
        }

        resp = client.post('/categories', data)
        assert_ok_created(resp.status_code)
        json_data = loads(resp.data.decode())
        assert 'id' in json_data

        TestCategory.new_id = json_data['id']

        resp = client.get('/categories/%d' % TestCategory.new_id)
        assert resp.status_code == HTTPStatus.OK
        category = loads(resp.data.decode())
        assert category['name'] == data['name']
        assert category['description'] == data['description']

    def test_category_add_invalid(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        data = {
            'name': None,
            'description': 'Missing category name'
        }

        resp = client.post('/categories', data)
        assert_error_response(resp)

    def test_category_edit(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        data = {
            'name': 'Edited category name',
            'description': 'Edited category description'
        }

        resp = client.put('/categories/%d' % TestCategory.new_id, data)
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/categories/%d' % TestCategory.new_id)
        assert resp.status_code == HTTPStatus.OK
        category = loads(resp.data.decode())
        assert category['name'] == data['name']
        assert category['description'] == data['description']

    def test_category_edit_invalid(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        data = {
            'name': None,
            'description': 'Invalid edit - no name'
        }

        resp = client.put('/categories/%d' % TestCategory.new_id, data)
        assert_error_response(resp)

    def test_category_edit_propagation(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        CATEGORY = category_fable
        BOOK = book_Animal_Farm

        data = {
            'name': 'Fairy tale',
            'description': 'Fantastical story'
        }

        resp = client.put('/categories/%d' % CATEGORY.id, data)
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/books/%d' % BOOK.id)
        assert resp.status_code == HTTPStatus.OK
        book = loads(resp.data.decode())
        category = find_by_id(CATEGORY.id, book['categories'])
        assert category is not None
        assert category['name'] == data['name']
        # assert category['description'] == data['description']
        # in book object  categories does not include descriptions

    def test_category_delete(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        resp = client.delete('/categories/%d' % TestCategory.new_id, {})
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/categories/%d' % TestCategory.new_id)
        assert_error_response(resp)

    def test_category_delete_propagation(self, client: ClientWrapper):
        client.login(user=user_employee_Brno)

        CATEGORY = category_fable
        BOOK = book_Animal_Farm

        resp = client.get('/books/%d' % BOOK.id)
        assert resp.status_code == HTTPStatus.OK
        book = loads(resp.data.decode())
        category = find_by_id(CATEGORY.id, book['categories'])
        assert category is not None

        resp = client.delete('/categories/%d' % CATEGORY.id, {})
        assert resp.status_code == HTTPStatus.OK

        resp = client.get('/books/%d' % BOOK.id)
        assert resp.status_code == HTTPStatus.OK
        book = loads(resp.data.decode())
        category = find_by_id(CATEGORY.id, book['categories'])
        assert category is None
