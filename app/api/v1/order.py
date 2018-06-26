from flask import request, json
from datetime import datetime, timedelta
from flask_restplus import Namespace, Resource
from app.models import Order, Dish, OrderItem, db
from time import strptime
from app.login import login_required
from flask_login import current_user
from app.models import *
import random

api = Namespace('orders')

@api.route('/test/')
class Orders(Resource):
    def get(self):
        try:
            # 新建菜单
            menu = Menu.query.filter_by(id=100).first()
            if menu is not None:
                return {'message':'Menu already exist.'}, 200
            menu = Menu()
            menu.id = 100
            menu.name = '测试菜单'
            menu.used = 1
            menu.delete = False
            menu.restId = 1
            db.session.add(menu)
            db.session.commit()

            # 新建2个类别, 每个类别4个菜
            cat1 = Category()
            cat1.id = 100
            cat1.name = '荤菜'
            cat1.rank = 0
            cat1.delete = False
            cat1.menuId = 100
            db.session.add(cat1)
            db.session.commit()
            for j in [0, 1, 2, 3]:
                dish = Dish()
                dish.id = 100 + j
                dish.name = '荤菜' + str(j)
                dish.rank = j
                dish.price = 15 + j * 5
                dish.avaliable = 1
                dish.stock = 99
                dish.likes = j * 2 + 5
                dish.description = '荤菜' + str(j)
                dish.delete = False
                dish.catId = 100
                db.session.add(dish)
                db.session.commit()

            cat2 = Category()
            cat2.id = 101
            cat2.name = '素菜'
            cat2.rank = 0
            cat2.delete = False
            cat2.menuId = 100
            db.session.add(cat2)
            db.session.commit()
            for j in [0, 1, 2, 3]:
                dish = Dish()
                dish.id = 104 + j
                dish.name = '素菜' + str(j)
                dish.rank = j
                dish.price = 35 + j * 5
                dish.avaliable = 1
                dish.stock = 99
                dish.likes = j * 2 + 5
                dish.description = '素菜' + str(j)
                dish.delete = False
                dish.catId = 101
                db.session.add(dish)
                db.session.commit()

            # menuid=100, catid=100, 101, dishid=100,101,102,103,104,105,106,107
            #                             price = 15, 20, 25, 30, 35, 40, 45, 50
            # 新建1200个用户，userid=[1000, 2199]
            for i in range(1000, 2200):
                user = User()
                user.id = i
                user.username = 'username' + str(i)
                user.authority = 'customer'
                db.session.add(user)
                db.session.commit()

            # 从今天起, 前60天, 每天30-50订单
            today = datetime.today()
            for i in range(0, 60):
                day = today + timedelta(days = -i)

                order_num = random.randint(30, 50)
                # 生成order_num个订单
                for j in range(order_num):
                    price = 0
                    # 选1-3个菜
                    dish_num = random.randint(1, 3)
                    dishes = []
                    items = []
                    for k in range(dish_num):
                        # 选一个菜id
                        dishid = random.randint(100, 107)
                        dish = Dish.query.filter_by(id=dishid).first()
                        dishes.append(dish)
                        # 有30%的概率点2份
                        quantity = 1
                        if random.random() < 0.3:
                            quantity = 2
                        price += dish.price * quantity
                        
                        orderitem = OrderItem()
                        orderitem.dishId = dishid
                        orderitem.quantity = quantity
                        orderitem.finished = 1
                        orderitem.time = day
                        items.append(orderitem)

                    order = Order()
                    # 选一个用户
                    order.uid = random.randint(1000, 2199)
                    order.tableId = 'SB'
                    order.total = price
                    order.due = price
                    order.isPay = 1
                    order.payId = 'Fake pay'
                    order.payWay = 'Bitcoin'
                    order.payDate = day
                    order.finished = 1
                    for dish in dishes:
                        order.dishes.append(dish)
                    db.session.add(order)
                    db.session.commit()
                    for item in items:
                        item.orderId = order.id
                        db.session.add(item)
                        db.session.commit()
            return {'message': 'Create fake data successfully.'}, 200
        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/cuser/')
class Orders(Resource):

    # 新建订单
    @login_required(authority='customer')
    def post(self):

        try:
            form = request.get_json(force=True)
            # form = request.form
            # print(form)
            tableId = form.get('tableId')
            if tableId is None:
                return {'message': 'Table\'s id is required'}, 400

            isPay = 0

            total = 0
            # dishesId = list(map(int, form.get('dishes').strip().split(',')))
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

            due = total
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
            orders =[]
            tmp = Order.query.filter_by(uid=current_user.id).all()
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
                return {'message': 'Wrong pay id'}, 400

            order = Order.query.filter_by(id=oid).first()
            if order is None:
                return {'message': 'Order not found.'}, 404
            if order.uid != current_user.id:
                return {'message': 'Wrong order id'}, 400

            if order.isPay:
                return {'message': 'Order is paid already.'}, 400

            order.payDate = datetime.now()
            order.payId = payId
            order.isPay = 1
            order.payWay = 'WeChat Pay'
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
            if order is None:
                return {'message': 'Order not found'}, 404
            if order.uid != current_user.id:
                return {'message': 'Wrong order id'}, 400

            return order.json(), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    # 用户修改订单
    @login_required(authority='customer')
    def put(self, oid):

        try:
            order = Order.query.filter_by(id=oid).first()
            if order is None:
                return {'message': 'Order not found'}, 404
            if order.uid != current_user.id:
                return {'message': 'Wrong order id'}, 400
            if order.isPay == 0:
                return {'message': 'Order not paid'}, 400

            form = request.get_json(force=True)
            dishId = form.get('dishId')
            if dishId is None:
                return {'message': 'Dish id is required'}, 400
            try:
                dishId = int(dishId)
            except Exception as e:
                print(e)
                return {'message': 'Wrong dish id'}, 400

            items = order.items
            found = False
            for item in items:
                if item.dishId == dishId:
                    dish = Dish.query.filter_by(id=dishId).first()
                    found = True
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
                        if item.like == 0 and like == 1:
                            dish.like += 1
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
                        item.urge = urge

                    db.session.commit()
                    break

            if found is False:
                return {'message': 'Dish not found'}, 404
            else:
                return {'message': 'Successfully modify.'}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500


@api.route('/buser/oid/<int:oid>')
class Orders(Resource):

    # 商家修改订单
    @login_required(authority='cook')
    def put(self, oid):

        order = Order.query.filter_by(id=oid).first()

        try:
            if order is None:
                return {'message': 'Order not found'}, 404
            if order.isPay == 0:
                return {'message': 'Order not paid'}, 400

            form = request.get_json(force=True)
            dishId = form.get('dishId')
            if dishId is None:
                return {'message': 'Dish id is required'}, 400
            try:
                dishId = int(dishId)
            except Exception as e:
                print(e)
                return {'message': 'Wrong dish id'}, 400

            items = order.items
            found = False
            for item in items:
                if item.dishId == dishId:
                    found = True
                    finished = form.get('finished')
                    if finished is not None:
                        try:
                            finished = int(finished)
                        except Exception as e:
                            print(e)
                            return {
                                'message': 'Finished should be 0 or 1, 1 means finished'
                                }, 400
                        if finished != 0 and finished != 1:
                            return {
                                'message': 'Finished should be 0 or 1, 1 means finished'
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

                    db.session.commit()
                    break

            finished = 1
            for item in items:
                if item.finished == 0:
                    finished = 0
                    break
            order.finished = finished
            db.session.commit()

            if found is False:
                return {'message': 'Dish not found'}, 404
            else:
                return {'message': 'Successfully modify.'}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

    # 商家获取单个订单
    @login_required(authority='cook')
    def get(self, oid):

        try:
            order = Order.query.filter_by(id=oid).first()

            if order is None:
                return {'message': 'Order not found '}, 404

            return order.json(), 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500

@api.route('/buser/')
class Orders(Resource):

    # 商家获取全部订单
    @login_required(authority='cook')
    def get(self):
        try:
            orders = Order.query.all()

            ret = []
            for order in orders:
                ret.append(order.json())

            return {'orders': ret}, 200

        except Exception as e:
            print(e)
            return {'message': 'Internal Server Error'}, 500
