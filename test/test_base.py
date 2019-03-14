import unittest
from api import create_api, app_dict


class QueryTestCase(unittest.TestCase):

    # we don't need to restore the db on each test, since we only allow read access...
    def setUp(self):
        create_api(True)
        self.app = app_dict['app'].test_client()

    def test_init(self):
        rv = self.app.get('/query/select * from block limit 1')
        assert b'486604799' in rv.data
        assert b'"difficulty": 1.0' in rv.data
        assert b'"id": 1' in rv.data


if __name__ == '__main__':
    unittest.main()
