from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource

api = Namespace('dishes')

@api.route('/')
class Dishes(Resource):

    def get(self):
        print(g.json)

        return {}, 200, None