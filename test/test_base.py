import unittest
import json
from api import create_api, app_dict


class QueryTestCase(unittest.TestCase):

    # we don't need to restore the db on each test,
    # since we only allow read access...
    def setUp(self):
        create_api(True)
        self.app = app_dict['app'].test_client()

    def test_simple_query(self):
        request = self.app.get('/query/select * from block limit 2')
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 200
        data = json.loads(request.data.decode('utf-8'))
        assert data[0]["id"] == 1
        assert data[0]["block_hash"] == "b'AAAAALhz55eEZHpsgpYscNIoVX0kp0fqTRuLvoeOEgY='"
        assert data[0]["difficulty"] == 1.0
        assert data[0]["height"] == 1
        assert data[0]["nonce"] == 1924588547
        assert data[0]["size"] == 190
        assert data[0]["version"] == 1
        assert data[0]["time"] == "2011-02-03T00:22:08"
        assert data[0]["merkleroot"] == "b'8DFf/DhwnXCtVkfiIEg1jdN0Xzzjh0IjyAp8kvqwyLo='"

        assert data[1]["id"] == 2

    def test_simple_error(self):
        request = self.app.get('/query/select')
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 200
        data = json.loads(request.data.decode('utf-8'))
        self.assertIn("You have an error in your SQL syntax;", data['error'])

    def test_encoder(self):
        request = self.app.get('/query/select * from vout limit 1')
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 200
        data = json.loads(request.data.decode('utf-8'))
        assert data[0]["txid"] == 1
        assert data[0]["value"] == 50


if __name__ == '__main__':
    unittest.main()
