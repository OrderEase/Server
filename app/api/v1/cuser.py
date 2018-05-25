from flask import request
from datetime import datetime, timedelta
from app.models import db, User
from flask_restplus import Namespace, Resource
from flask_login import login_user, logout_user, current_user
from app.login import login_required

api = Namespace('cuser')

@api.route('/session')
class CuserLogin(Resource):

	def post(self):
		''' log in '''
		try:
			form = request.form
			username = form.get('username')
			if username is None:
				return {'message': 'Username is required.'}, 400

			role = form.get('role')
			if role is None:
				return {'message': 'User role is required.'}, 400

			if role != "CUSTOMER":
				return {'message': 'User role must be CUSTOMER.'}, 400

			user = User.query.filter_by(username=username).first()

			if user is None:
				new_user = User(username=username, password='', role="CUSTOMER")
				db.session.add(new_user)
				db.session.commit()
				user = new_user

			login_user(user)
			# print(current_user)
			return {'message': 'Successfully login.'}, 200

		except Exception as e:
			print(e)
			return {'message': 'Internal Server Error'}, 500


	@login_required(role="CUSTOMER")
	def put(self):
		''' log out '''
		logout_user()

		return {'message': "Successfully logout."}, 200





