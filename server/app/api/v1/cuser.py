from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource

api = Namespace('cuser')

@api.route('/login')
class CuserLogin(Resource):

	def post(self):
		data = request.data
		username = data.username
		return None, 200, None

@api.route('/logout')
class CuserLogout(Resource):

	def put(self):

		return None, 200, None





