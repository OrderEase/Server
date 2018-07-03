from flask import request
from datetime import datetime, timedelta
from app.models import db, User
from flask_restplus import Namespace, Resource
from flask_login import login_user, logout_user, current_user
from app.login import login_required

api = Namespace('cusers')

@api.route('/session')
class CuserLog(Resource):

	def post(self):
		''' log in '''
		try:
			form = request.get_json(force=True)

			username = form.get('username')
			if username is None:
				print('ee')
				return {'message': 'Username is required.'}, 400

			cuser = User.query.filter_by(username=username).first()

			if cuser is None:
				new_user = User(username=username, password='', authority="customer")
				db.session.add(new_user)
				db.session.commit()
				cuser = new_user

			login_user(cuser)
			return {'message': 'Successfully login.'}, 200

		except Exception as e:
			print(e)
			return {'message': 'Internal Server Error'}, 500


	@login_required(authority="customer")
	def put(self):
		''' log out '''
		logout_user()

		return {'message': "Successfully logout."}, 200





