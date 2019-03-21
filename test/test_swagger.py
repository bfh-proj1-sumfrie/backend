import unittest
import json
from api import create_api


class QueryTestCase(unittest.TestCase):

    # we don't need to restore the db on each test,
    # since we only allow read access...
    def setUp(self):
        app = create_api(True)
        self.app = app.test_client()

    def test_swagger(self):
        request = self.app.get('api/swagger.json')
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 200
        data = json.loads(request.data.decode('utf-8'))
        assert data["swagger"] == '2.0'
        assert data["paths"]["/query"]["post"]["description"] == "Returns an sql query result"
        assert data["paths"]["/query"]["post"]["parameters"][0]["in"] == "body"
        assert data["definitions"]["RequestQueryModel"]["type"] == "object"
        sql = data["definitions"]["RequestQueryModel"]["properties"]["sql"]
        assert sql["type"] == "string"
        assert sql["default"] == "select * from block limit 10"


if __name__ == '__main__':
    unittest.main()
