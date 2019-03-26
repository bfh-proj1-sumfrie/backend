import unittest
import json
from api import create_api


class QueryTestCase(unittest.TestCase):

    def setUp(self):
        app = create_api(True)
        self.app = app.test_client()

    def test_update(self):
        request = self.app.post('/query',
                                data='{"sql": "UPDATE CUSTOMERS SET ADDRESS = 123 WHERE ID = 6;"}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 401
        data = json.loads(request.data.decode('utf-8'))
        assert data['error'] == "The following keyword is not allowed: update"

    def test_delete(self):
        request = self.app.post('/query',
                                data='{"sql": "DELETE FROM CUSTOMERS WHERE ID = 6;"}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 401
        data = json.loads(request.data.decode('utf-8'))
        assert data['error'] == "The following keyword is not allowed: delete"

    def test_alter(self):
        request = self.app.post('/query',
                                data='{"sql": "ALTER TABLE table_name ADD column_name datatype;"}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 401
        data = json.loads(request.data.decode('utf-8'))
        assert data['error'] == "The following keyword is not allowed: alter"

    def test_truncate(self):
        request = self.app.post('/query',
                                data='{"sql": "TRUNCATE TABLE  table_name;"}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 401
        data = json.loads(request.data.decode('utf-8'))
        assert data['error'] == "The following keyword is not allowed: truncate"


if __name__ == '__main__':
    unittest.main()
