from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import Rstr, db, Menu, Dish

api = Namespace('rstr')

@api.route('/<int:rstrid>')
class Rstrs(Resource):

    def post(self, rstrid):
        try:
            rstr = Rstr.query.filter_by(id=rstrid).first()
            if rstr is None:
                return {'message': 'Rstr not found'}, 404

            form = request.form
            name = form.get('name')
            menu = Menu()
            menu.name = name
            menu.rstr_id = rstr.id
            rstr.menus.append(menu)

            dishesId = list(map(int, form.get('dishes').strip().split(',')))
            dishes = []
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


    def get(self, rstrid):
        try:
            rstr = Rstr.query.filter_by(id=rstrid).first()
            if rstr is None:
                return {'message': 'Rstr not found'}, 404

            return rstr.json(), 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/')
class Rstrs(Resource):
    def post(self):
        try:
            form = request.form
            name = form.get('name')
            exist = Rstr.query.filter_by(name=name).first()
            if exist is not None:
                return {'message': 'Rstr name already exist'}, 400
            if name is None:
                return {'message': 'Rstr name is required'}, 400

            info = form.get('info')
            if info is None:
                return {'message': 'Rstr info is required'}, 400

            rstr = Rstr()
            rstr.name = name
            rstr.info = info
            db.session.add(rstr)
            db.session.commit()

            return {'rstrId': rstr.id}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500
