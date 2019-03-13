import datetime
import decimal
from flask_restful import Resource, Api
from flask import Flask, json
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from api.database import engine


def create_api():
    app = Flask(__name__)
    api = Api(app)

    class QueryResource(Resource):
        def get(self, sql):
            sql = text(sql)
            try:
                db_response = engine.execute(sql)
            except SQLAlchemyError as err:
                return json.jsonify({"error": str(err)})

            return [dict(r) for r in db_response]

    api.add_resource(QueryResource, '/query/<string:sql>')

    # JSON encoder function for SQLAlchemy special classes
    def alchemy_encoder(obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, decimal.Decimal):
            return float(obj)

    return app

