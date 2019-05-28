"""
 Author: Elias Summermatter & Jan Friedli
 Date: 28.05.2019
 Licence:
 This file is part of BloSQL.
 BloSQL is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.
 BloSQL is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.
 You should have received a copy of the GNU General Public License
 along with BloSQL.  If not, see <http://www.gnu.org/licenses/>.
 Code partly adapted from:
 - http://flask.pocoo.org/docs/1.0/testing/
 """

import unittest
import json
from api import create_api


class QueryTestCase(unittest.TestCase):

    # we don't need to restore the db on each test,
    # since we only allow read access...
    def setUp(self):
        app = create_api(True)
        self.app = app.test_client()

    def test_simple_query(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from block limit 2", "page": 0, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 200
        data = json.loads(request.data.decode('utf-8'))['data']
        assert data[0]["id"] == 1
        assert data[0]["block_hash"] == "00000000b873e79784647a6c82962c70d228557d24a747ea4d1b8bbe878e1206"
        assert data[0]["difficulty"] == 1.0
        assert data[0]["height"] == 1
        assert data[0]["nonce"] == 1924588547
        assert data[0]["size"] == 190
        assert data[0]["version"] == 1
        assert data[0]["time"] == "2011-02-03T00:22:08"
        assert data[0]["merkleroot"] == "f0315ffc38709d70ad5647e22048358dd3745f3ce3874223c80a7c92fab0c8ba"

        assert data[1]["id"] == 2

    def test_simple_query_with_semicolon(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from block limit 2;", "page": 0, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 200
        data = json.loads(request.data.decode('utf-8'))['data']
        assert data[0]["id"] == 1
        assert data[0]["block_hash"] == "00000000b873e79784647a6c82962c70d228557d24a747ea4d1b8bbe878e1206"
        assert data[0]["difficulty"] == 1.0
        assert data[0]["height"] == 1
        assert data[0]["nonce"] == 1924588547
        assert data[0]["size"] == 190
        assert data[0]["version"] == 1
        assert data[0]["time"] == "2011-02-03T00:22:08"
        assert data[0]["merkleroot"] == "f0315ffc38709d70ad5647e22048358dd3745f3ce3874223c80a7c92fab0c8ba"
        assert data[1]["id"] == 2

    def test_simple_error(self):
        request = self.app.post('/query',
                                data='{"sql": "select", "page": 0, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )

        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 400
        data = json.loads(request.data.decode('utf-8'))
        self.assertIn("You have an error in your SQL syntax;", data['message'])

    def test_request_error(self):
        request = self.app.post('/query',
                                data='{"page": 0, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )

        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 400
        data = json.loads(request.data.decode('utf-8'))
        assert data['message']["sql"] == "sql is not valid string or not present"

    def test_encoder(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from vout limit 1", "page": 0, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        data = json.loads(request.data.decode('utf-8'))['data']
        assert request.status_code == 200
        assert data[0]["txid"] == 1
        assert data[0]["value"] == 50

    def test_multiple_queries(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from vout limit 1; select * from block limit 10",'
                                     '"page": 0, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        data = json.loads(request.data.decode('utf-8'))
        assert request.status_code == 400
        self.assertIn('You have an error in your SQL syntax', data['message'])

    def test_multiple_queries_correct_syntax(self):
        request = self.app.post('/query',
                                data='{"sql": "select * from vout limit 1; select * from block limit 10;"'
                                     ', "page": 0, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        data = json.loads(request.data.decode('utf-8'))
        assert request.status_code == 400
        self.assertIn('ou have an error in your SQL syntax', data['message'])

    def test_show_tables(self):
        request = self.app.post('/query',
                                data='{"sql": "show tables", "page": 0, "pageSize": 10}',
                                headers={'content-type': 'application/json'}
                                )
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 200
        data = json.loads(request.data.decode('utf-8'))['data']
        assert len(data) == 8

    def test_404(self):
        request = self.app.get('/some-random-that-does-not-exist')
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 404
        data = json.loads(request.data.decode('utf-8'))
        assert data['message'] == "The requested URL was not found on the server. If you entered the" \
                                  " URL manually please check your spelling and try again."


if __name__ == '__main__':
    unittest.main()
