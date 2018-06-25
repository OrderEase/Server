from flask import request, g
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import User, Restaurant, db
from flask_login import login_user, logout_user, current_user
from app.login import login_required
from PIL import Image
import hashlib
from .utils import getImageFromBase64

api = Namespace('busers')

@api.route('/')
class BUserRegister(Resource):

    def post(self):
        """新建商家用户
        """
        try:
            form = request.form

            username = form.get('username')
            if username is None:
                return {'message': 'Username is required.'}, 400

            password = form.get('password')
            if username is None:
                return {'message': 'Password is required.'}, 400

            authority = form.get('authority')
            if authority != "manager" and authority != "cook":
                return {'message': 'Invalid authority. Required "manager" or "cook"'}, 400

            buser = User.query.filter_by(username=username).first()
            if buser is not None:
                return {'message': 'Username exists.'}, 400

            new_buser = User(username=username, password=password, authority=authority)
            db.session.add(new_buser)
            db.session.commit()

            return {"message": "Successfully register."}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/password')
class BUserModifyPassword(Resource):

    @login_required(authority="manager")
    def post(self):
        try:
            form = request.form

            password = form.get('password')
            if password is None:
                return {'message': 'Password is required.'}, 400

            buser = User.query.get(current_user.id)
            buser.password = password
            db.session.commit()

            return {"message": "Change password successfully."}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/session')
class BUserLog(Resource):

    def post(self):
        """log in """
        try:
            form = request.form

            username = form.get('username')
            if username is None:
                return {'message': 'Username is required.'}, 400

            password = form.get('password')
            if username is None:
                return {'message': 'Password is required.'}, 400

            buser = User.query.filter_by(username=username).first()
            if buser is None or buser.password != password:
                return {"message": "Invalid username or password."}, 401

            login_user(buser)

            return {"message": "Successfully login."}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    @login_required(authority="manager")
    def put(self):
        """Log out
        """
        logout_user()

        return {'message': "Successfully logout."}, 200

