from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource

api = Namespace('rstr')

@api.route('/')
class Rstr(Resource):

    def post(self):
        print(g.json)

        return {}, 200, None