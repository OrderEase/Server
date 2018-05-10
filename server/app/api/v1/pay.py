from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource

api = Namespace('pay')

@api.route('/')
class Pay(Resource):

    def post(self):
        print(g.json)

        return None, 200, None