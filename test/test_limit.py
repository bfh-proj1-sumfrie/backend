# import unittest
# import json
# from api import create_api
#
#
# class QueryTestCase(unittest.TestCase):
#
#     def setUp(self):
#         app = create_api(True)
#         self.app = app.test_client()
#
#     def test_no_limit(self):
#         request = self.app.post('/query',
#                                 data='{"sql": "select * from block"}',
#                                 headers={'content-type': 'application/json'}
#                                 )
#         assert request.headers['Content-Type'] == 'application/json'
#         assert request.status_code == 200
#         data = json.loads(request.data.decode('utf-8'))
#         assert len(data) == 10
#
#     def test_limit_too_high(self):
#         request = self.app.post('/query',
#                                 data='{"sql": "select * from block limit 100000000000000000000"}',
#                                 headers={'content-type': 'application/json'}
#                                 )
#         assert request.headers['Content-Type'] == 'application/json'
#         assert request.status_code == 200
#         data = json.loads(request.data.decode('utf-8'))
#         assert len(data) == 10
#
#     def test_limit_smaller_than_config(self):
#         request = self.app.post('/query',
#                                 data='{"sql": "select * from block limit 2"}',
#                                 headers={'content-type': 'application/json'}
#                                 )
#         assert request.headers['Content-Type'] == 'application/json'
#         assert request.status_code == 200
#         data = json.loads(request.data.decode('utf-8'))
#         assert len(data) == 2
#
#     def test_limit_comma_style(self):
#         request = self.app.post('/query',
#                                 data='{"sql": "select * from block limit 1 offset 1"}',
#                                 headers={'content-type': 'application/json'}
#                                 )
#         assert request.headers['Content-Type'] == 'application/json'
#         assert request.status_code == 200
#         data = json.loads(request.data.decode('utf-8'))
#         assert data[0]['id'] == 2
#
#
# if __name__ == '__main__':
#     unittest.main()
