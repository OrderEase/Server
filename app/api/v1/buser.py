from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import User, Rstr, db
from flask_login import login_user, logout_user, current_user
from app.login import login_required

api = Namespace('buser')

@api.route('/')
class BUserRegister(Resource):

    def post(self):
        """新建商家用户
        """
        try:
            form = request.form

            role = form.get('role')
            if role is None:
                return {'message': 'User role is required.'}, 400

            if role != "BUSINESS":
                return {'message': 'User role must be BUSINESS.'}, 400

            username = form.get('username')
            if username is None:
                return {'message': 'Username is required.'}, 400

            password = form.get('password')
            if username is None:
                return {'message': 'Password is required.'}, 400

            authority = form.get('authority')
            if authority != "MANAGER" and authority != "COOK":
                return {'message': 'Invalid authority. Required "MANAGER" or "COOK"'}, 400

            rstr_id = form.get('restId')
            if rstr_id is None:
                return {'message': 'Resturant id is required.'}, 400
            rstr = Rstr.query.get(rstr_id)
            if rstr is None:
                return {"message": "Restaurant not found."}, 404

            buser = User.query.filter_by(username=username).first()
            if buser is not None:
                return {'message': 'Username exists.'}, 400

            new_buser = User(username=username, password=password, role=role, authority=authority, rstr_id=rstr_id)
            db.session.add(new_buser)
            db.session.commit()

            return {"message": "Successfully register."}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/<userId>')
class BUserModifyPassword(Resource):

    @login_required(role="BUSINESS")
    def post(self):
        try:
            form = request.form

            password = form.get('password')
            if password is None:
                return {'message': 'Password is required.'}, 400


            buser = User.query.get(current_user.id)
            buser.password = password
            db.session.add(buser)
            db.session.commit()

            return {"message": "Change password successfully."}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

        return None, 200, None

@api.route('/session')
class BUserLog(Resource):

    def post(self):
        try:
            form = request.form

            role = form.get('role')
            if role is None:
                return {'message': 'User role is required.'}, 400

            if role != "BUSINESS":
                return {'message': 'User role must be BUSINESS.'}, 400

            username = form.get('username')
            if username is None:
                return {'message': 'Username is required.'}, 400

            password = form.get('password')
            if username is None:
                return {'message': 'Password is required.'}, 400

            rstr_id = form.get('restId')
            if rstr_id is None:
                return {'message': 'Resturant id is required.'}, 400

            rstr = Rstr.query.get(rstr_id)
            if rstr is None:
                return {"message": "Restaurant not found."}, 404

            buser = User.query.filter_by(username=username).first()
            if buser is None:
                return {"message": "Username not exist."}, 401

            if buser.password != password:
                return {"message": "Wrong password."}, 401

            login_user(buser)

            return {"message": "Successfully login.", "buser_id": buser.id}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    @login_required(role="BUSINESS")
    def put(self):
        """Log out
        """
        logout_user()

        return {'message': "Successfully logout."}, 200

