import unittest
import json
from api import create_api
from os import environ


class SchemaTestCase(unittest.TestCase):
    def setUp(self):
        environ.setdefault("LIMITER_PER_HOUR_VAL", "2")
        app = create_api(True)
        self.app = app.test_client()

    def test_limit(self):
        self.app.post('/query')
        self.app.post('/query')

        # the 3 request which needs to be blocked
        request = self.app.post('/query')
        data = json.loads(request.data.decode('utf-8'))
        assert request.headers['Content-Type'] == 'application/json'
        assert request.status_code == 429
        assert data['message'] == "2 per 1 hour"

    def tearDown(self):
        environ.setdefault("LIMITER_PER_HOUR_VAL", "1000000")


if __name__ == '__main__':
    unittest.main()
