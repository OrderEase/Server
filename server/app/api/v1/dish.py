from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import Dish, db

api = Namespace('dish')

@api.route('/')
class Dishes(Resource):

    def post(self):
        
        try:
            form = request.form
            name = form.get('name')
            exist = Dish.query.filter_by(name=name).first()
            if exist is not None:
                return {'message': 'Dish name already exist'}, 400
            if name is None:
                return {'message': 'Dish name is required'}, 400

            category = form.get('category')
            if category is None:
                category = 'other'

            price = float(form.get('price'))
            if price is None or price < 0:
                return {'message': 'Price is required and not negative.'}, 400

            stock = int(form.get('stock'))
            if stock is None:
                stock = 0
            if stock < 0:
                return {'message': 'Stock can not be negative.'}, 400

            avaliable = (form.get('avaliable') == 'True')

            likes = int(form.get('likes'))
            if likes is None:
                likes = 0
            if likes < 0:
                return {'message': 'Likes can not be negative.'}, 400

            description = form.get('description')
            if description is None:
                description = ""

            dish = Dish()
            dish.name = name
            dish.category = category
            dish.price = price
            dish.stock = stock
            dish.avaliable = avaliable
            dish.likes = likes
            dish.description = description
            db.session.add(dish)
            db.session.commit()

            return {'dishId': dish.id}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/did/<int:did>')
class Dishes(Resource):
    def get(self, did):
        dish = Dish.query.filter_by(id=did).first()
        if dish is None:
            return {'message': 'Dish not found'}, 404

        return dish.json(), 200

    def put(self, did):
        dish = Dish.query.filter_by(id=did).first()
        if dish is None:
            return {'message': 'Dish not found'}, 404

        try:
            form = request.form
            name = form.get('name')
            if name is None:
                return {'message': 'Dish name is required'}, 400

            category = form.get('category')
            if name is None:
                category = 'other'

            price = float(form.get('price'))
            if price is None or price < 0:
                return {'message': 'Price is required and not negative.'}, 400

            stock = int(form.get('stock'))
            if stock is None:
                stock = 0
            if stock < 0:
                return {'message': 'Stock can not be negative.'}, 400

            avaliable = (form.get('avaliable') == 'True')

            likes = int(form.get('likes'))
            if likes is None:
                likes = 0
            if likes < 0:
                return {'message': 'Likes can not be negative.'}, 400

            description = form.get('description')
            if description is None:
                description = ""

            dish.name = name
            dish.category = category
            dish.price = price
            dish.stock = stock
            dish.avaliable = avaliable
            dish.likes = likes
            dish.description = description
            db.session.commit()

            return {'message': 'Successfully update.', 'dishId': dish.id}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500  

    def delete(self, did):
        dish = Dish.query.filter_by(id=did).first()
        if dish is None:
            return {'message': 'Dish not found'}, 404
        db.session.delete(dish)
        db.session.commit()
        return {'message': 'Successfully delete.'}, 200

@api.route('/category/<string:cat>')
class Dishes(Resource):     
    def get(self, cat):
        
        try:
            if cat is None:
                cat = 'other'

            dishes =[]
            tmp = Dish.query.filter_by(category=cat).all()
            if tmp is None:
                return {'message': 'Dishes not found'}, 404
            for dish in tmp:
                dishes.append(dish.json())

            return {'category': cat,
                     'dishes': dishes}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500