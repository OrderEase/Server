from flask import request, json
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from sqlalchemy import desc
from app.models import Promotion, Order, Dish, OrderItem, db
from time import strptime
from app.login import login_required
from flask_login import current_user
from app.models import *
import random
from sqlalchemy import desc

api = Namespace('orders')

@api.route('/cuser/')
class Orders(Resource):

    # 新建订单
    @login_required(authority='customer')
    def post(self):

        try:
            form = request.get_json(force=True)

            tableId = form.get('tableId')
            if tableId is None:
                return {'message': 'Table\'s id is required'}, 400

            isPay = 0

            total = 0
            contents = form.get('content')
            dishes = []
            items = []
            for item in contents:
                try:
                    did = int(item['dish'])
                except Exception as e:
                    print(e)
                    return {'message': 'Dish id should be integer'}, 400

                try:
                    quantity = int(item['quantity'])
                except Exception as e:
                    print(e)
                    return {'message': 'Quantity should be integer'}, 400

                dish = Dish.query.filter_by(id=did).first()
                if dish is None:
                    return {'message': 'Dish (id: %i) is not found' % (did)}, 404
                total += dish.price * quantity

                dishes.append(dish)

                item = OrderItem()
                item.dishId = did
                item.quantity = quantity
                item.finished = 0
                item.urge = 0
                item.like = 0
                items.append(item)

            promotions = Promotion.query.filter(Promotion.isend == 0).all()
            best_due = total
            for promotion in promotions:
                for rule in promotion.rules:
                    if total < rule.requirement:
                        continue
                    current_due = 0
                    if rule.mode == 1:
                        current_due = total - rule.discount
                    elif rule.mode == 2:
                        current_due = total * rule.discount

                    if current_due < best_due:
                        best_due = current_due

            due = best_due
            t_total = form.get('total')
            if t_total is None:
                return {'message': 'Total is required'}, 400
            if t_total != total:
                return {'message': 'Total is wrong, check it!'}, 400

            t_due = form.get('due')
            if t_due is None:
                return {'message': 'Due is required'}, 400
            if t_due != due:
                return {'message': 'Due is wrong, check it!'}, 400

            order = Order()
            order.tableId = tableId
            order.total = total
            order.due = due
            order.isPay = isPay

            order.uid = current_user.id
            for dish in dishes:
                order.dishes.append(dish)
            db.session.add(order)
            db.session.commit()

            for item in items:
                item.orderId = order.id
                db.session.add(item)
                db.session.commit()

            return {'id': order.id}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    # 用户获取全部订单
    @login_required(authority='customer')
    def get(self):
        try:
            orders = []
            tmp = Order.query.filter_by(uid=current_user.id).filter_by(Cdelete=False).order_by(desc(Order.payDate)).all()

            for order in tmp:
                orders.append(order.json())

            return {'orders': orders}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/cuser/oid/<int:oid>')
class Orders(Resource):

    # 用户付款
    @login_required(authority='customer')
    def post(self, oid):

        try:
            form = request.get_json(force=True)
            payId = form.get('payId')
            if payId is None:
                print('Wrong pay id')
                return {'message': 'Wrong pay id'}, 400

            order = Order.query.filter_by(id=oid).first()
            if order is None:
                print('1')
                return {'message': 'Order not found.'}, 404
            if order.uid != current_user.id:
                return {'message': 'Wrong order id'}, 400

            if order.isPay:
                print('2')
                return {'message': 'Order is paid already.'}, 400

            payWay = form.get('payWay')
            if payWay is None:
                print('3')
                return {'message': 'Pay way is required.'}, 400

            order.payDate = datetime.now()
            order.payId = payId
            order.isPay = 1
            # payWays = ['微信支付', '比特币', '支付宝', '银行卡']
            # payWay = random.randint(0, 3)
            order.payWay = payWay
            db.session.commit()

            return {"message": "Successfully pay."}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    # 用户获取单个订单
    @login_required(authority='customer')
    def get(self, oid):
        try:
            order = Order.query.filter_by(id=oid).first()
            if order is None or order.Cdelete == True:
                return {'message': 'Order not found'}, 404
            if order.uid != current_user.id:
                return {'message': 'Wrong order id'}, 400

            return order.json(), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    # 用户删除单个订单
    @login_required(authority='customer')
    def delete(self, oid):
        try:
            order = Order.query.filter_by(id=oid).first()
            if order is None or order.Cdelete == True:
                return {'message': 'Order not found'}, 404
            if order.uid != current_user.id:
                return {'message': 'Wrong order id'}, 400

            order.Cdelete = True

            return order.json(), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    # 用户修改订单
    @login_required(authority='customer')
    def put(self, oid):

        try:
            order = Order.query.filter_by(id=oid).first()
            if order is None or order.Cdelete == True:
                return {'message': 'Order not found'}, 404
            if order.uid != current_user.id:
                return {'message': 'Wrong order id'}, 400
            if order.isPay == 0:
                return {'message': 'Order not paid'}, 400

            form = request.get_json(force=True)
            orderItemId = form.get('orderItemId')
            if orderItemId is None:
                return {'message': 'orderItemId is required'}, 400
            try:
                orderItemId = int(orderItemId)
            except Exception as e:
                print(e)
                return {'message': 'Wrong dish id'}, 400

            item = OrderItem.query.filter_by(id=orderItemId).first()
            if item is None:
                return {'message': 'Dish not found'}, 404
            dish = Dish.query.filter_by(id=item.dishId).first()
            like = form.get('like')
            if like is not None:
                try:
                    like = int(like)
                except Exception as e:
                    print(e)
                    return {
                        'message': 'Like should be 0 or 1, 1 means like'
                        }, 400
                if like != 0 and like != 1:
                    return {
                        'message': 'Like should be 0 or 1, 1 means like'
                        }, 400
                if item.like == 1 and like == 1:
                    return {
                        'message': 'Already like'
                    }, 400
                if item.like == 0 and like == 1:
                    dish.likes += 1
                item.like = like

            urge = form.get('urge')
            if urge is not None:
                try:
                    urge = int(urge)
                except Exception as e:
                    print(e)
                    return {
                        'message': 'Urge should be 0 or 1, 1 means urge'
                        }, 400
                if urge != 0 and urge != 1:
                    return {
                        'message': 'Urge should be 0 or 1, 1 means urge'
                        }, 400
                if urge == 1 and item.urge == 1:
                    return {
                        'message': 'Already urge'
                    }, 400
                if item.finished == 1 and urge == 1:
                    return {
                        'message': 'Dish is already finished'
                    }, 400
                item.urge = urge

            db.session.commit()

            return {'message': 'Successfully modify.'}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500


@api.route('/buser/oid/<int:oid>')
class Orders(Resource):

    # 商家修改订单
    @login_required(authority='cook')
    def put(self, oid):

        try:
            order = Order.query.filter_by(id=oid).first()
            if order is None:
                return {'message': 'Order not found'}, 404
            if order.isPay == 0:
                return {'message': 'Order not paid'}, 400

            form = request.get_json(force=True)

            orderItemId = form.get('orderItemId')
            if orderItemId is None:
                return {'message': 'orderItemId is required'}, 400
            try:
                orderItemId = int(orderItemId)
            except Exception as e:
                print(e)
                return {'message': 'Wrong dish id'}, 400

            item = OrderItem.query.filter_by(id=orderItemId).first()
            if item is None:
                return {'message': 'Dish not found'}, 404
            dish = Dish.query.filter_by(id=item.dishId).first()
            finished = form.get('finished')
            if finished is not None:
                try:
                    finished = int(finished)
                except Exception as e:
                    print(e)
                    return {
                        'message': 'finished should be 0 or 1, 1 means finished'
                        }, 400
                if finished != 0 and finished != 1:
                    return {
                        'message': 'finished should be 0 or 1, 1 means finished'
                        }, 400
                item.finished = finished

            time = form.get('time')
            if time is not None:
                try:
                    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    print(e)
                    return {
                        'message': 'Wrong date-time format'
                        }, 400
                item.time = time

            finished = 1
            items = order.items
            for item in items:
                if item.finished == 0:
                    finished = 0
                    break
            order.finished = finished

            db.session.commit()

            return {'message': 'Successfully modify.'}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    # 商家获取单个订单
    @login_required(authority='cook')
    def get(self, oid):

        try:
            order = Order.query.filter_by(id=oid).first()

            if order is None or (order.Cdelete == True and order.isPay == 0):
                return {'message': 'Order not found '}, 404

            return order.json(), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/buser')
class Orders(Resource):

    # 商家获取全部订单
    @login_required(authority='cook')
    def get(self):
        try:
            finished = request.args.get('finished')
            if finished is None:
                orders = Order.query.filter_by(isPay=1).order_by(Order.payDate)
            else:
                finished = int(finished)
                orders = Order.query.filter_by(finished=finished).filter_by(isPay=1).order_by(Order.payDate)
            ret = []
            for order in orders:
                ret.append(order.json())

            return {'orders': ret}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500
