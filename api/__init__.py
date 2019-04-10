from flask_restful import Resource, reqparse, abort, Api
from flask import Flask, json, make_response
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from api.encoder import alchemy_encoder
from flask_sqlalchemy import SQLAlchemy
from api.database import get_db_connection_uri
from flask_cors import CORS
from api.param_validator import validate_pagesize_param


def create_api(is_test=False):
    app = Flask(__name__)
    api = Api(app, catch_all_404s=True)
    CORS(app, resources={r"/*": {"origins": "*"}})

    if is_test:
        app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_connection_uri(is_test)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    class QueryResource(Resource):
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('sql', type=str, required=True, help='sql is not valid string or not present')
            parser.add_argument('pageSize', type=int, required=True, help='pageSize param must be set in body')
            parser.add_argument('page', type=int, required=True, help='page param must be set in body')
            args = parser.parse_args()

            validate_pagesize_param(args['pageSize'])
            offset = args["page"] * args['pageSize']
            pagination = dict()

            try:
                # there is no validation of the sql since this is a task for the db admins!
                result = []
                db_response = db.engine.execute(text(args['sql']))
                db.engine.execution_options()
                idx = 0
                pagination['page'] = args["page"]
                pagination['max_pages'] = int(db_response.rowcount / args['pageSize'])

                if pagination['max_pages'] > 0:
                    pagination['max_pages'] -= 1

                if args["page"] > pagination['max_pages']:
                    abort(400, message='This page does not exist')

                for entry in db_response:
                    if offset <= idx < (offset + args['pageSize']):
                        result.append(dict(entry))
                    idx += 1
            except SQLAlchemyError as err:
                return abort(400, message=str(err))

            data = dict()
            data['pagination'] = pagination
            data['data'] = result

            json_data = json.dumps(data, default=alchemy_encoder)
            response = make_response(json_data)
            response.mimetype = 'application/json'

            return response

    class SchemaResource(Resource):
        def get(self):
            try:
                tables = db.engine.execute(text('SHOW TABLES;'))
                response = []

                for table in tables:
                    columns = db.engine.execute(text('SHOW COLUMNS FROM ' + table[0] + ';'))
                    response.append({
                        "table_name": table[0],
                        "columns": [dict(row) for row in columns]
                    })

                return response

            except SQLAlchemyError as err:
                return abort(400, message=str(err))

    api.add_resource(QueryResource, '/query')
    api.add_resource(SchemaResource, '/schema')

    return app
