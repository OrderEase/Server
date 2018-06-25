from flask import request
from datetime import datetime, timedelta, time
from flask_restplus import Namespace, Resource
from app.models import Restaurant, db, Menu, Dish
from app.login import login_required

api = Namespace('restrt')

@api.route('/')
class Rstrs(Resource):

    # 获取餐馆信息
    @login_required(authority='customer')
    def get(self):
        try:
            rstr = Restaurant.query.filter_by(id=1).first()
            if rstr is None:
                return {'message': 'Restaurant not found'}, 404

            return rstr.json(), 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    # 修改餐馆信息
    @login_required(authority='manager')
    def put(self):
        try:
            rstr = Restaurant.query.filter_by(id=1).first()
            if rstr is None:
                return {'message': 'Restaurant not found'}, 404

            form = request.get_json(force=True)
            name = form.get('name')
            if name is not None:
                rstr.name = name

            description = form.get('description')
            if description is not None:
                rstr.description = description

            img = form.get('img')
            if img is not None:
                rstr.img = img
            
            open = form.get('open')
            if open is not None:
                try:
                    open = datetime.strptime(open, "%H:%M:%S")
                except Exception as e:
                    print(e)
                    return {'message': 'Wrong format of time'}, 400
                rstr.open = open
            
            close = form.get('close')
            if close is not None:
                try:
                    close = datetime.strptime(close, "%H:%M:%S")
                except Exception as e:
                    print(e)
                    return {'message': 'Wrong format of time'}, 400
                rstr.close = close

            db.session.commit()

            return {'message': 'Modify restaurant info successfully'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500
