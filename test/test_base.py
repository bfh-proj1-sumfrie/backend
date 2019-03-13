from api import create_api
import unittest


class QueryTestCase(unittest.TestCase):

    def setUp(self):
        app = create_api()
        app.testing = True
        self.app = app.test_client()

    def test_init(self):
        rv = self.app.get('/query/test')
        assert b'test' in rv.data


if __name__ == '__main__':
    unittest.main()
