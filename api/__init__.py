import os
from flask_restful import Resource, reqparse
from flask import Flask, json, make_response
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from api.encoder import alchemy_encoder
from flask_sqlalchemy import SQLAlchemy
from api.database import get_db_connection_uri
from flask_restful_swagger_2 import Api, swagger, Schema


def create_api(is_test=False):
    app = Flask(__name__)
    api = Api(app, api_version='0.1', api_spec_url='/api/swagger', host=os.environ.get('API_HOST', 'localhost:5000'))

    if is_test:
        app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_connection_uri(is_test)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    class RequestQueryModel(Schema):
        # needed for swagger only
        type = 'object'
        properties = {
            'sql': {
                'type': 'string',
                'default': 'select * from block limit 10'
            }
        }
        required = ['sql']

    class QueryResource(Resource):
        # use post because there is no limit in sql length
        # (get has a length limit of ca. 2000 chars)
        # and its easier in case of special chars
        # this is actually not fully HTTP compliant
        @swagger.doc({
            'tags': ['sql'],
            'description': 'Returns an sql query result',
            'parameters': [
                {
                    'name': 'sql query',
                    'description': 'The sql query to run',
                    'in': 'body',
                    'schema': RequestQueryModel
                }
            ],
            'responses': {
                '200': {
                    'description': 'Valid Request',
                    'examples': {
                        'application/json': [
                            {
                                "bits": 486604799,
                                "block_hash": "b'AAAAALhz55eEZHpsgpYscNIoVX0kp0fqTRuLvoeOEgY='",
                                "difficulty": 1,
                                "height": 1,
                                "id": 1,
                                "merkleroot": "b'8DFf/DhwnXCtVkfiIEg1jdN0Xzzjh0IjyAp8kvqwyLo='",
                                "nonce": 1924588547,
                                "prev_block_hash": "b'AAAAAAkz6gGtDumEIJd5uq7DztkPo/QIcZUm+Nd/SUM='",
                                "size": 190,
                                "time": "2011-02-03T00:22:08",
                                "version": 1
                            },
                            {
                                "bits": 486604799,
                                "block_hash": "b'AAAAAGwCyOpuT/aWUff83jSPudVXoG5pV7ZVUgAqeCA='",
                                "difficulty": 1,
                                "height": 2,
                                "id": 2,
                                "merkleroot": "b'ICIuuQ9YlVVpJsESu1qg30q1q8MQfiGmlQrsOy41QeI='",
                                "nonce": 875942400,
                                "prev_block_hash": "b'AAAAALhz55eEZHpsgpYscNIoVX0kp0fqTRuLvoeOEgY='",
                                "size": 190,
                                "time": "2011-02-03T00:22:26",
                                "version": 1
                            },
                        ]
                    }
                },
                '400': {
                    'description': 'Bad Request',
                    'examples': {
                        'message': {
                            'sql': "sql is not valid string or not present"
                        }
                    }
                }
            }
        })
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('sql', type=str, required=True, help='sql is not valid string or not present')
            args = parser.parse_args()

            try:
                db_response = db.engine.execute(text(args['sql']))
            except SQLAlchemyError as err:
                return json.jsonify({"error": str(err)})

            data = json.dumps([dict(r) for r in db_response], default=alchemy_encoder)
            response = make_response(data)
            response.mimetype = 'application/json'
            response.headers['Access-Control-Allow-Origin'] = '*'

            return response

    api.add_resource(QueryResource, '/query')

    return app
