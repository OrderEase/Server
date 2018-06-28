from .models import User, Order, Dish, OrderItem, Menu, Category, Restaurant, db
from datetime import datetime, timedelta

import random

def remove_data():
    db.drop_all()

def gen_basic_data():
    try:
        # db.drop_all()
        db.create_all()
        user = User.query.filter_by(id=1).first()
        if user is not None:
            print("Basic data exists.")
            return

        print("Generating basic data...")

        today = datetime.today()

        buser_manager = User()
        buser_manager.id = 1
        buser_manager.username = "manager"
        buser_manager.password = "123"
        buser_manager.authority = "manager"
        buser_manager.register_date = today + timedelta(days=-7)
        db.session.add(buser_manager)

        buser_cook = User()
        buser_cook.id = 2
        buser_cook.username = "cook"
        buser_cook.password = "123"
        buser_cook.authority = "cook"
        buser_cook.register_date = today + timedelta(days=-7)
        db.session.add(buser_cook)
        db.session.commit()

        restrt = Restaurant()
        restrt.id = 1
        restrt.name = "四饭"
        restrt.open = today + timedelta(days=-30)
        restrt.close = today + timedelta(days=30)
        restrt.description = "就近原则"
        db.session.add(restrt)
        db.session.commit()

    except Exception as e:
        print(e)
        print('Internal Server Error')


def gen_fake_data():
    try:
        # db.drop_all()
        db.create_all()
        user = User.query.filter_by(id=2199).first()
        if user is not None:
            print("Database is not empty. Stop generating fake data.")
            return

        print("Generating fake data...")

        today = datetime.today()

        menu = Menu.query.filter_by(id=100).first()
        if menu is not None:
            print('Menu already exist.')
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
        cat2.rank = 1
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

        cat3 = Category()
        cat3.id = 102
        cat3.name = '小吃'
        cat3.rank = 2
        cat3.delete = False
        cat3.menuId = 100
        db.session.add(cat3)
        db.session.commit()
        for j in [0, 1, 2, 3]:
            dish = Dish()
            dish.id = 108 + j
            dish.name = '小吃' + str(j)
            dish.rank = j
            dish.price = 15 + j * 5
            dish.avaliable = 1
            dish.stock = 99
            dish.likes = j * 2 + 5
            dish.description = '小吃' + str(j)
            dish.delete = False
            dish.catId = 102
            db.session.add(dish)
            db.session.commit()

        cat4 = Category()
        cat4.id = 103
        cat4.name = '酒水'
        cat4.rank = 3
        cat4.delete = False
        cat4.menuId = 100
        db.session.add(cat4)
        db.session.commit()
        for j in [0, 1, 2, 3]:
            dish = Dish()
            dish.id = 112 + j
            dish.name = '酒水' + str(j)
            dish.rank = j
            dish.price = 15 + j * 20
            dish.avaliable = 1
            dish.stock = 99
            dish.likes = j * 2 + 5
            dish.description = '酒水' + str(j)
            dish.delete = False
            dish.catId = 103
            db.session.add(dish)
            db.session.commit()

        cat5 = Category()
        cat5.id = 104
        cat5.name = '炖汤'
        cat5.rank = 4
        cat5.delete = False
        cat5.menuId = 100
        db.session.add(cat5)
        db.session.commit()
        for j in [0, 1, 2, 3]:
            dish = Dish()
            dish.id = 116 + j
            dish.name = '炖汤' + str(j)
            dish.rank = j
            dish.price = 15 + j * 6
            dish.avaliable = 1
            dish.stock = 99
            dish.likes = j * 2 + 5
            dish.description = '炖汤' + str(j)
            dish.delete = False
            dish.catId = 104
            db.session.add(dish)
            db.session.commit()

        # menuid=100, catid=100, 101, dishid=100-119
        #                             price = 15, 20, 25, 30, 35, 40, 45, 50
        # 新建1200个 customer，userid=[1000, 2199]

        for i in range(1000, 2200):
            user = User()
            user.id = i
            user.username = 'username' + str(i)
            user.authority = 'customer'
            user.register_date = today + timedelta(days=int((random.random() - 1) * 30))
            db.session.add(user)
            db.session.commit()

        payWays = ['微信支付', '比特币', '支付宝', '银行卡']
        # 从今天起, 前60天, 每天30-50订单

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

                order_time = day + timedelta(minutes=random.random() * 1440)
                for k in range(dish_num):
                    # 选一个菜id
                    dishid = random.randint(100, 119)
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
                    orderitem.time = order_time + timedelta(minutes=random.random() * 30)
                    items.append(orderitem)

                order = Order()
                # 选一个用户
                order.uid = random.randint(1000, 2199)
                order.tableId = 'SB'
                order.total = price
                order.due = price
                order.isPay = 1
                order.payId = 'Fake pay'
                payWay = random.randint(0, 3)
                order.payWay = payWays[payWay]
                order.payDate = order_time
                order.finished = 1
                for dish in dishes:
                    order.dishes.append(dish)
                db.session.add(order)
                db.session.commit()
                for item in items:
                    item.orderId = order.id
                    db.session.add(item)
                    db.session.commit()
        print('Create fake data successfully.')
        db.session.remove()

    except Exception as e:
        print(e)
        print('Internal Server Error')

def gen_unfinished_orders():
    try:
        # db.drop_all()
        db.create_all()

        print("Generating unfinished orders...")

        today = datetime.today()

        payWays = ['微信支付', '比特币', '支付宝', '银行卡']
        # 从今天起, 前60天, 每天30-50订单

        day = today

        order_num = random.randint(15, 25)
        # 生成order_num个订单
        for j in range(order_num):
            price = 0
            # 选1-3个菜
            dish_num = random.randint(1, 3)
            dishes = []
            items = []

            order_time = day + timedelta(minutes=random.random() * 1440)
            for k in range(dish_num):
                # 选一个菜id
                dishid = random.randint(100, 119)
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
                orderitem.finished = 0
                items.append(orderitem)

            order = Order()
            # 选一个用户
            order.uid = random.randint(1000, 2199)
            order.tableId = 'SB'
            order.total = price
            order.due = price
            order.isPay = 1
            order.payId = 'Fake pay'
            payWay = random.randint(0, 3)
            order.payWay = payWays[payWay]
            order.payDate = order_time
            order.finished = 0
            for dish in dishes:
                order.dishes.append(dish)
            db.session.add(order)
            db.session.commit()
            for item in items:
                item.orderId = order.id
                db.session.add(item)
                db.session.commit() 
        print('Create unfinished orders successfully.')
        db.session.remove()

    except Exception as e:
        print(e)
        print('Internal Server Error')