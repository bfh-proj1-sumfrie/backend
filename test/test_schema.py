import unittest
import json
from api import create_api


class SchemaTestCase(unittest.TestCase):
    def setUp(self):
        app = create_api(True)
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
