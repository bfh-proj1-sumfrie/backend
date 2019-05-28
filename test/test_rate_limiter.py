""""
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
from api.api import create_api
from os import environ


class SchemaTestCase(unittest.TestCase):

    def test_limit_query(self):
        environ.setdefault("LIMITER_PER_HOUR_VAL", "2")
        app = create_api(True)
        self.app = app.test_client()

        self.app.post('/query')
        self.app.post('/query')

        # the 3 request which needs to be blocked
        request = self.app.post('/query')
        data = json.loads(request.data.decode('utf-8'))
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 429
        assert data['message'] == "2 per 1 hour"

    def test_limit_schema(self):
        environ.setdefault("LIMITER_PER_HOUR_VAL", "2")
        app = create_api(True)
        self.app = app.test_client()

        self.app.get('/schema')
        self.app.get('/schema')

        # the 3 request which needs to be blocked
        request = self.app.get('/schema')
        data = json.loads(request.data.decode('utf-8'))
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 429
        assert data['message'] == "2 per 1 hour"

    def tearDown(self):
        environ.setdefault("LIMITER_PER_HOUR_VAL", "1000000")


if __name__ == '__main__':
    unittest.main()
