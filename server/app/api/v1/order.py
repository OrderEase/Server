from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import Order, Dish, db

api = Namespace('order')

@api.route('/cuid/<int:cuid>')
class Orders(Resource):
	def post(self, cuid):

		try:
            form = request.form
            tableId = form.get('tableId')
            if tableId is None:
                return {'message': 'Table\'s id is required'}, 400

            order = Order()
            order.tableId = tableId
		    isPay = False
		    payWay = 'Not yet pay'
		    payDate = strptime("1979-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

    		total = 0
            dishes = list(map(int, form.get('dishes').strip().split(',')))
            for did in dishes:
				dish = Dish.query.filter_by(id=did).first()
				if dish is None:
					return {'message': 'Dish (id: %i) is not found' % (did)}
				total += dish.price
            	order.dishes.append(dish)

            due = total

            order.tableId = tableId
		    order.total = total
		    order.due = due
		    order.isPay = isPay
		    order.payWay = payWay
		    order.payDate = payDate
		    db.session.add(order)
            db.session.commit()

            return {'orderId': order.id}, 200
        except Exception as e:
            print e
            return {'message': 'Internal Server Error'}, 500

	def get(self, cuid):
		try:
            orders =[]
            tmp = Order.query.filter_by(uid=cuid).all()
            for order in tmp:
                orders.append(order.json())

            return {'orders': orders}, 200

        except Exception as e:
            print e
            return {'message': 'Internal Server Error'}, 500

@api.route('/cuid/<int:cuid>/oid/<int:oid>')
class Orders(Resource):
	def put(self, cuid, oid):

		try:
			form = request.form
			payId = form.get('payId')
			if payId is None:
				return {'message': 'pay id is wrong or not exist.'}, 400

			order = Order.filter_by(id=oid).first()
			if order is None:
				return {'message': 'Order not found.'}, 404

			if order.isPay:
				return {'message': 'Order is paid already.'}, 400

			order.payId = payId
			order.payDate = datetime.now()
			order.isPay = True
			db.session.commit()

		except Exception as e:
            print e
            return {'message': 'Internal Server Error'}, 500
