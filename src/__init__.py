from flask import Flask
from flask_restful import Resource, Api


def create_api():
    app = Flask(__name__)
    api = Api(app)

    class QueryResource(Resource):
        def get(self, sql):
            return {"test": sql}

    api.add_resource(QueryResource, '/query/<string:sql>')

    return app
