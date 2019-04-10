import unittest
import json
from api import create_api


class SchemaTestCase(unittest.TestCase):
    def setUp(self):
        app = create_api(True)
        self.app = app.test_client()

    def test_valid_schema_get(self):
        for i in range(0, 500):
            self.app.get('/schema')

        # the 1001 request which needs to be blocked
        request = self.app.get('/schema')
        data = json.loads(request.data.decode('utf-8'))
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 429
        assert data['message'] == "500 per 1 hour"


if __name__ == '__main__':
    unittest.main()
