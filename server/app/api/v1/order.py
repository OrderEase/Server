from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource

api = Namespace('order')

@api.route('/<id>')
class Order(Resource):
	def get(self, id):

		# get order from db
		# dish = Dish.query.get

		return {'id' : 3910,
				'name' : 'simpledish',
				'category' : 'huncai',
				'price' : 28.5,
				'stock' : 99,
				'avaliable' : 'true',
				'likes' : 4,
				'description' : 'hello, dish.'
				}, 200

	def post(self):
		form = request.form

		print(request.form)
		id = form.get('id')
		print(id)

		# dishes = form.get('dishes')
		# for dish in dishes:
		# 	print(dish['id'])

		return {"orderId": 4396}, 200

	def put(self):
		form = request.form
		id_ = form.get('id')
		print(id_)

		return {}, 200