from flask import request, g
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import User, Restaurant, db
from flask_login import login_user, logout_user, current_user
from app.login import login_required
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import hashlib
from .utils import getImageFromBase64

api = Namespace('busers')

@api.route('/password')
class BUserModifyPassword(Resource):

    @login_required(authority="manager")
    def put(self):
        try:
            form = request.get_json(force=True)

            old_password = form.get('oldPassword')
            if old_password is None:
                return {'message': 'Old password is required.'}, 400

            new_password = form.get('newPassword')
            if new_password is None:
                return {'message': 'New password is required.'}, 400

            buser = User.query.get(current_user.id)
            # print(current_user.username)
            if not check_password_hash(buser.password, old_password):
                return {'message': 'Old password wrong.'}, 401

            buser.password = generate_password_hash(new_password)
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
            form = request.get_json(force=True)

            username = form.get('username')
            if username is None:
                return {'message': 'Username is required.'}, 400

            password = form.get('password')
            if username is None:
                return {'message': 'Password is required.'}, 400

            buser = User.query.filter_by(username=username).first()
            if buser is None or not check_password_hash(buser.password, password):
                return {"message": "Invalid username or password."}, 401

            login_user(buser)

            return {"message": "Successfully login.", "authority": buser.authority}, 200

        except Exception as e:
            return {'message': 'Internal Server Error'}, 500

    @login_required(authority='cook')
    def put(self):
        """Log out
        """
        logout_user()

        return {'message': "Successfully logout."}, 200

