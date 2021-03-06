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
 - https://flask-restful.readthedocs.io/en/latest/quickstart.html#a-minimal-api
 - https://flask-restful.readthedocs.io
 - https://flask-cors.readthedocs.io/en/latest/
 - https://pypi.org/project/Flask-Limiter/
"""

from os import environ
from flask_restful import Resource, reqparse, abort, Api
from flask import Flask, json, make_response
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from api.encoder import alchemy_encoder
from flask_sqlalchemy import SQLAlchemy
from api.database import get_db_connection_uri
from flask_cors import CORS
from api.param_validator import validate_pagesize_param
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_app(is_test=False):
    app = Flask(__name__)
    api = Api(app, catch_all_404s=True)
    CORS(app, resources={r"/*": {"origins": "*"}})
    Limiter(
        app,
        key_func=get_remote_address,
        default_limits=[
            environ.get('LIMITER_PER_DAY_VAL', "10000") + " per day",
            environ.get('LIMITER_PER_HOUR_VAL', "500") + " per hour"
        ]
    )

    if is_test:
        app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_connection_uri(is_test)
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = int(environ.get('github', 60))
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
            tables = db.engine.execute(text('SHOW TABLES;'))
            response = []

            for table in tables:
                columns = db.engine.execute(text('SHOW COLUMNS FROM ' + table[0] + ';'))
                response.append({
                    "table_name": table[0],
                    "columns": [dict(row) for row in columns]
                })

            return response

    api.add_resource(QueryResource, '/query')
    api.add_resource(SchemaResource, '/schema')

    return app
