from flask import request
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import Order, Dish, db
from time import strptime
from app.login import login_required


api = Namespace('order')

@api.route('/cuid/<int:cuid>')
class Orders(Resource):

    # 新建订单
    @login_required(authority="customer", userID_field_name="cuid")
    def post(self, cuid):

        try:
            form = request.form
            tableId = form.get('tableId')
            if tableId is None:
                return {'message': 'Table\'s id is required'}, 400

            order = Order()
            isPay = False
            payWay = 'Not yet pay'
            payDate = datetime.now()

            total = 0
            dishesId = list(map(int, form.get('dishes').strip().split(',')))
            dishes = []
            for did in dishesId:
                dish = Dish.query.filter_by(id=did).first()
                if dish is None:
                    return {'message': 'Dish (id: %i) is not found' % (did)}, 404
                total += dish.price
                dishes.append(dish)

            due = total

            order.tableId = tableId
            order.total = total
            order.due = due
            order.isPay = isPay
            order.payWay = payWay
            order.payDate = payDate
            order.uid = cuid
            for dish in dishes:
                order.dishes.append(dish)
            db.session.add(order)
            db.session.commit()

            return {'orderId': order.id}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    @login_required(authority="customer", userID_field_name="cuid")
    def get(self, cuid):
        try:
            orders =[]
            tmp = Order.query.filter_by(uid=cuid).all()
            for order in tmp:
                orders.append(order.json())

            return {'orders': orders}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/cuid/<int:cuid>/oid/<int:oid>')
class Orders(Resource):

    @login_required(authority="customer", userID_field_name="cuid")
    def put(self, cuid, oid):

        try:
            form = request.form
            payId = form.get('payId')
            if payId is None:
                return {'message': 'pay id is wrong or not exist.'}, 400

            order = Order.query.filter_by(id=oid).first()
            if order is None:
                return {'message': 'Order not found.'}, 404

            if order.isPay:
                return {'message': 'Order is paid already.'}, 400

            order.payDate = datetime.now()
            order.isPay = True
            order.payWay = 'WeChat Pay'
            db.session.commit()

            return {"message": "Successfully pay."}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    @login_required(authority="customer", userID_field_name="cuid")
    def get(self, cuid, oid):
        try:
            order = Order.query.filter_by(id=oid).first()
            if order is None:
                return {'message': 'Order not found'}, 404

            return order.json(), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500
