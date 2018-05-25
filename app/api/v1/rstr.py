from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import Rstr, db, Menu, Dish
from app.login import login_required

api = Namespace('rstr')

@api.route('/')
class Rstrs(Resource):

    # 获取餐馆信息和菜单
    # @login_required(role='BUSSINESS')
    def get(self):
        try:
            rstr = Rstr.query.filter_by(id=1).first()
            if rstr is None:
                return {'message': 'Rstr not found'}, 404

            return rstr.json(), 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/buid/<int:buid>')
class Rstrs(Resource):

    # 修改餐馆信息
    # @login_required(role='BUSSINESS', userID_field_name='buid')
    def put(self):
        try:
            rstr = Rstr.query.filter_by(id=1).first()
            if rstr is None:
                return {'message': 'Rstr not found'}, 404

            form = request.form
            name = form.get('name')
            if name is None:
                return {'message': 'Rstr name is required'}, 400

            info = form.get('info')
            if info is None:
                return {'message': 'Rstr info is required'}, 400

            rstr.name = name
            rstr.info = info
            db.session.add(rstr)
            db.session.commit()

            return {'message': 'Modify rstr info successfully'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500
    
@api.route('/buid/<int:buid>/menu')
class Rstrs(Resource):

    # 新建菜单
    # @login_required(role='BUSSINESS', userID_field_name='buid')
    def post(self):
        try:
            rstr = Rstr.query.filter_by(id=1).first()
            if rstr is None:
                return {'message': 'Rstr not found'}, 404

            form = request.form
            name = form.get('name')

            tmp = Menu.query.filter_by(name=name).first()
            if tmp is not None:
                return {'message': 'Name already exists.'}, 400

            menu = Menu()
            menu.name = name
            menu.rstr_id = 1
            rstr.menus.append(menu)

            dishesId = list(map(int, form.get('dishes').strip().split(',')))
            for did in dishesId:
                dish = Dish.query.filter_by(id=did).first()
                if dish is None:
                    return {'message': 'Dish (id: %i) is not found' % (did)}, 404
                menu.dishes.append(dish)

            db.session.add(menu)     
            db.session.commit()

            return {'message': 'Add a new menu successfully.'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/buid/<int:buid>/menu/<menuId>')
class Rstrs(Resource):

    # 修改菜单
    # @login_required(role='BUSSINESS', userID_field_name='buid')
    def put(self):
        try:

            menu = Menu.query.filter_by(id=menuId).first()
            if menu is None:
                return {'message': 'Menu not found'}, 404

            form = request.form
            name = form.get('name')

            tmp = Menu.query.filter_by(name=name).first()
            if tmp is not None:
                return {'message': 'Name already exists.'}, 400

            menu.name = name

            dishesId = list(map(int, form.get('dishes').strip().split(',')))
            menu.dishes.clear()
            for did in dishesId:
                dish = Dish.query.filter_by(id=did).first()
                if dish is None:
                    return {'message': 'Dish (id: %i) is not found' % (did)}, 404
                menu.dishes.append(dish)
   
            db.session.commit()

            return {'message': 'Modify a new menu successfully.'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500