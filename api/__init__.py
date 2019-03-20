from flask_restful import Resource, Api, reqparse
from flask import Flask, json, make_response
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from api.encoder import alchemy_encoder
from flask_sqlalchemy import SQLAlchemy
from api.database import get_db_connection_uri


def create_api(is_test=False):
    app = Flask(__name__)
    api = Api(app)

    if is_test:
        app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_connection_uri(is_test)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    class QueryResource(Resource):
        # use post because there is no limit in sql length (get has a length limit of ca. 2000 chars)
        # and its easier in case of special chars
        # this is actually not fully HTTP compliant
        def post(self):
            parser = reqparse.RequestParser()
            parser.add_argument('sql', type=str, help='sql is no valid string')
            args = parser.parse_args()

            sql = text(args['sql'])
            try:
                db_response = db.engine.execute(sql)
            except SQLAlchemyError as err:
                return json.jsonify({"error": str(err)})

            data = json.dumps([dict(r) for r in db_response], default=alchemy_encoder)
            response = make_response(data)
            response.mimetype = 'application/json'
            return response

    api.add_resource(QueryResource, '/query')

    return app

