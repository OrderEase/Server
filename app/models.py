from datetime import datetime, date
# from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), doc='用户名', unique=True)
    password = db.Column(db.String(32), doc='密码', nullable=True)
    avatar = db.Column(db.String(100), doc='头像路径', nullable=True, default='default.png')
    authority = db.Column(db.String(32), doc='权限, [customer, manager, cook]', nullable=False)

    def __repr__(self):
        tmp = {
            'id': self.id,
            'username': self.username,
            'authority': self.authority
        }
        return '{id}: 用户 {username}, 权限 {authority} '.format(**tmp)

    def json(self):
        return {
            'id': self.id
        }

orders_dishes = db.Table('orders_dishes',
    db.Column('orderId', db.Integer, db.ForeignKey('orders.id')),
    db.Column('dishId', db.Integer, db.ForeignKey('dishes.id'))
)

class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    tableId = db.Column(db.String(32), nullable=False)
    total = db.Column(db.Float, nullable=False)
    due = db.Column(db.Float, nullable=False)
    isPay = db.Column(db.Integer, default=0, nullable=False)
    payId = db.Column(db.String(32), nullable=True)
    payWay = db.Column(db.String(32), nullable=True)
    payDate = db.Column(db.DateTime, nullable=True)
    finished = db.Column(db.Integer, default=0, nullable=False)

    dishes = db.relationship('Dish', secondary=orders_dishes, lazy='dynamic',
        backref=db.backref('orders', lazy='dynamic'))
    uid = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)
    items = db.relationship('OrderItem', backref='orders', lazy='dynamic')

    def __repr__(self):
        tmp = {
            'payDate': self.payDate.strftime("%Y-%m-%d %H:%M:%S"),
            'id': self.id,
            'due': self.due,
            'total': self.total,
            'isPay': self.isPay,
            'payWay': self.payWay,
            'finished': self.finished
        }
        return ('{payDate}: order {id}, due is {due}, total is {total}\n'
                'isPay: {isPay}').format(**tmp)

    def json(self):
        t_dishes = []
        for dish in self.dishes:
            t_dishes.append(dish.json())

        t_orderItems = []
        for item in self.items:
            t_orderItems.append(item.json())

        return {
            'id': self.id,
            'tableId': self.tableId,
            'total': self.total,
            'due': self.due,
            'isPay': self.isPay,
            'payWay': str(self.payWay),
            'payDate': self.payDate.strftime("%Y-%m-%d %H:%M:%S"),
            'payId': self.payId,
            'dishes': t_dishes,
            'orderItems': t_orderItems
        }

class OrderItem(db.Model):

    __tablename__ = 'orderItems'

    id = db.Column(db.Integer, primary_key=True)
    orderId = db.Column(db.Integer, db.ForeignKey('orders.id'),
        nullable=False)
    dishId = db.Column(db.Integer, db.ForeignKey('dishes.id'))
    quantity = db.Column(db.Integer, nullable=False)
    finished = db.Column(db.Integer, default=0, nullable=False)
    time = db.Column(db.DateTime, nullable=True)
    urge = db.Column(db.Integer, default=0, nullable=False)
    like = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        tmp = {
            'id': self.id,
            'orderId': self.orderId,
            'dishId': self.dishId
        }
        return 'item {id}, order: {orderId}, dishId: {dishId}'.format(**tmp)

    def json(self):
        return {
            'id': self.id,
            'orderId': self.orderId,
            'dishId': self.dishId,
            'quantity': self.quantity,
            'finished': self.finished,
            'time': self.time.strftime("%Y-%m-%d %H:%M:%S"),
            'urge': self.urge,
            'like': self.like
        }

class Dish(db.Model):

    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    img = db.Column(db.String(256), nullable=True)
    price = db.Column(db.Float, nullable=False)
    avaliable = db.Column(db.Integer, default=0, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, default=0, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    delete = db.Column(db.Boolean, default=False, nullable=False)

    catId = db.Column(db.Integer, db.ForeignKey('categories.id'),
                        nullable=False)

    def __repr__(self):
        tmp = {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'avaliable': self.avaliable,
            'stock': self.stock,
            'likes': self.likes,
            'description': self.description
        }
        return ('id: {id}, name: {name}, price: {price}\n'
                'avaliable: {avaliable}, stock: {stock}, likes: {likes}\n'
                'description: {description}').format(**tmp)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'img': self.img,
            'rank': self.rank,
            'price': self.price,
            'avaliable': self.avaliable,
            'stock': self.stock,
            'likes': self.likes,
            'description': self.description
        }

class Category(db.Model):

    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    delete = db.Column(db.Boolean, default=False, nullable=False)

    dishes = db.relationship('Dish', backref='categories', lazy='dynamic')

    menuId = db.Column(db.Integer, db.ForeignKey('menus.id'),
                        nullable=False)

    def __repr__(self):
        tmp = {
            'id': self.id,
            'name': self.name,
            'rank': self.rank
        }
        return 'id: {id}, name: {name}, rank: {rank}'.format(**tmp)

    def json(self):
        t_dishes = []
        for dish in self.dishes:
            t_dishes.append(dish.json())

        return {
            'id': self.id,
            'name': self.name,
            'rank': self.rank,
            'dishes': t_dishes
        }

class Menu(db.Model):

    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    used = db.Column(db.Integer, default=0, nullable=False)
    delete = db.Column(db.Boolean, default=False, nullable=False)

    cats = db.relationship('Category', backref='menus', lazy='dynamic')
    restId = db.Column(db.Integer, db.ForeignKey('restaurant.id'),
                        nullable=False)

    def __repr__(self):
        tmp = {
            'id': self.id,
            'name': self.name,
            'used': self.used
        }
        return 'id: {id}, name: {name}, used: {uesed}'.format(**tmp)

    def json(self):
        content = []
        for cat in self.cats:
            content.append(cat.json())

        return {
            'id': self.id,
            'name': self.name,
            'used': self.used,
            'content': content
        }


class Promotion(db.Model):

    __tablename__ = 'promotion'

    id = db.Column(db.Integer, primary_key=True)
    theme = db.Column(db.String(32), nullable=False)
    begin = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    isend = db.Column(db.Integer, nullable=False)

    rules = db.relationship('Rule', backref='promotion', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)

    def __repr__(self):
        tmp = {
            'id': self.id,
            'theme': self.theme,
            'begin': self.begin.strftime("%Y-%m-%d %H:%M:%S"),
            'end': self.end.strftime("%Y-%m-%d %H:%M:%S"),
            'isend': self.isend
        }
        return 'id: {id}, 主题: {theme}, 开始时间: {begin}, 结束时间: {end}, 是否已结束: {isend}'.format(**tmp)

    def json(self):
        rules_list = []
        for rule in self.rules.all():
            rules_list.append(rule.json())

        return {
            'id': self.id,
            'theme': self.theme,
            'begin': self.begin.strftime("%Y-%m-%d %H:%M:%S"),
            'end': self.end.strftime("%Y-%m-%d %H:%M:%S"),
            'isend': self.isend,
            'rules': rules_list
        }


class Rule(db.Model):

    __tablename__ = 'rule'

    id = db.Column(db.Integer, primary_key=True)
    mode = db.Column(db.Integer, nullable=False)  # 1（满减），2（满折）
    requirement = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)

    promotion_id = db.Column(db.Integer, db.ForeignKey('promotion.id', ondelete='CASCADE'), nullable=False)

    def __repr__(self):
        tmp = {
            'id': self.id,
            'mode': '满减' if self.mode == 1 else '满折' if self.mode == 2 else 'error',
            'requirement': self.requirement,
            'discount': self.discount,
            'promotion_id': self.promotion_id
        }
        return 'id: {id}, 优惠条件: {mode}, 要求: {requirement}, 优惠: {discount}, 对应优惠id: {promotion_id}'.format(**tmp)

    def json(self):
        return {
            'id': self.id,
            'mode': self.mode,
            'requirement': self.requirement,
            'discount': self.discount,
        }


class Restaurant(db.Model):

    __tablename__ = 'restaurant'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    img = db.Column(db.String(256), nullable=True)
    open = db.Column(db.DateTime, nullable=True)
    close = db.Column(db.DateTime, nullable=True)

    menus = db.relationship('Menu', backref='restaurant',
                lazy='dynamic')
    cars = db.relationship('Carousel', backref='restaurant',
                lazy='dynamic')

    def __repr__(self):
        tmp = {
            'id': self.id,
            'name': self.name,
            'open': self.open.strftime("%Y-%m-%d %H:%M:%S"),
            'close': self.close.strftime("%Y-%m-%d %H:%M:%S")
        }
        return ('id: {id}, name: {name}, open: {open}\n'
                'close: {close}').format(**tmp)

    def json(self):
        # t_menus = []
        # for menu in self.menus:
        #     t_menus.append(menu.json())

        t_cars = []
        for car in self.cars:
            t_cars.append(car.json())

        return {
            'id': self.id,
            'name': self.name,
            'open': self.open.strftime("%Y-%m-%d %H:%M:%S"),
            'close': self.close.strftime("%Y-%m-%d %H:%M:%S"),
            'carousels': t_cars
            # 'menus': t_menus
        }

class Carousel(db.Model):

    __tablename__ = 'carousel'

    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(256), nullable=False)
    img = db.Column(db.String(256), nullable=False)

    restId = db.Column(db.Integer, db.ForeignKey('restaurant.id'),
                nullable=False)

    def json(self):
        return {
            'id': self.id,
            'info': self.info,
            'img': self.img
        }
