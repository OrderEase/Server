
from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource

api = Namespace('dish')

@api.route('/')
class Dish(Resource):

    def get(self):
        print(g.json)

        return {'name': 'something'}, 200, None

    def post(self):
        print(g.json)

        return {}, 400, None

    def put(self):
        print(g.json)

        return None, 200, None

    def delete(self):
        print(g.json)

        return None, 200, None