from flask_restful import Resource, Api
from flask import Flask, json, make_response
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from api.encoder import alchemy_encoder
from flask_sqlalchemy import SQLAlchemy
from api.database import get_db_connection_uri

app_dict = {}


def create_api(is_test=False):
    app = Flask(__name__)
    api = Api(app)

    if is_test:
        app.config['TESTING'] = True

    app.config['SQLALCHEMY_DATABASE_URI'] = get_db_connection_uri(is_test)
    db = SQLAlchemy(app)

    app_dict['app'] = app
    app_dict['db'] = db

    class QueryResource(Resource):
        def get(self, sql):
            sql = text(sql)
            try:
                db_response = db.engine.execute(sql)
            except SQLAlchemyError as err:
                return json.jsonify({"error": str(err)})

            data = json.dumps([dict(r) for r in db_response], default=alchemy_encoder)
            response = make_response(data)
            response.mimetype = 'application/json'
            return response

    api.add_resource(QueryResource, '/query/<string:sql>')

    return app

