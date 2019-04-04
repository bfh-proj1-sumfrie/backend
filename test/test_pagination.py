import unittest
import json
from api import create_api


class QueryTestCase(unittest.TestCase):

    # we don't need to restore the db on each test,
    # since we only allow read access...
    def setUp(self):
        app = create_api(True)
        self.app = app.test_client()

    def test_params_missing(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from block"}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        data = json.loads(request.data.decode('utf-8'))
        assert request.status_code == 400
        assert data['message']['pageSize'] == 'pageSize param must be set in body'

    def test_page_missing(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from block", "pageSize": 1}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        data = json.loads(request.data.decode('utf-8'))
        assert request.status_code == 400
        assert data['message']['page'] == 'page param must be set in body'

    def test_pageSize_missing(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from block", "page": 0}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        data = json.loads(request.data.decode('utf-8'))
        assert request.status_code == 400
        assert data['message']['pageSize'] == 'pageSize param must be set in body'

    def test_valid_query(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from block", "page": 0, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        data = json.loads(request.data.decode('utf-8'))
        assert request.status_code == 200
        assert len(data['data']) == 10
        assert data['data'][0]['id'] == 1
        assert data['data'][9]['id'] == 10
        assert data['pagination']['page'] == 0
        assert data['pagination']['max_pages'] == 1000

    def test_valid_query_with_offset(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from block", "page": 1, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        data = json.loads(request.data.decode('utf-8'))
        assert request.status_code == 200
        assert len(data['data']) == 10
        assert data['data'][0]['id'] == 11
        assert data['data'][9]['id'] == 20

    def test__query_with_large_offset(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from block", "page": 10000000000000000000, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        data = json.loads(request.data.decode('utf-8'))
        assert request.status_code == 400
        assert data['error'] == 'This page does not exist'

    def test__query_with_large_page_size(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from block", "page": 0, "pageSize": 10000000000000000000}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        data = json.loads(request.data.decode('utf-8'))
        assert request.status_code == 400
        assert data['error'] == 'The pageSize parameter cannot be greater than: 100'


if __name__ == '__main__':
    unittest.main()
