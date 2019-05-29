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
from api.api import create_app


class SchemaTestCase(unittest.TestCase):
    def setUp(self):
        app = create_app(True)
        self.app = app.test_client()

    def test_valid_schema_get(self):
        request = self.app.get('/schema')
        data = json.loads(request.data.decode('utf-8'))
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 200
        assert data[0]['table_name'] == "block"
        assert data[0]['columns'][0]["Field"] == "id"
        assert len(data) == 8
        for col in data[0]['columns']:
            assert len(col) == 6


if __name__ == '__main__':
    unittest.main()
