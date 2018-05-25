from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource

api = Namespace('buser')

@api.route('/')
class Buser(Resource):

    def put(self):
        print(g.json)

        return None, 200, None

@api.route('/login')
class BuserLogin(Resource):

    def post(self):
        print(g.json)

        return None, 200, None

@api.route('/logout')
class BuserLogout(Resource):

    def put(self):

        return None, 200, None

@api.route('/register')
class BuserRegister(Resource):

    def post(self):
        print(g.json)

        return None, 200, None