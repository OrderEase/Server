from datetime import datetime, date
# from app import db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), doc="用户名", unique=True)
    password = db.Column(db.String(32), doc='密码', nullable=True)
    role = db.Column(db.String(32), doc='用户类型', nullable=False)
    authority = db.Column(db.String(32), doc='商家权限', nullable=True)
    rstr_id = db.Column(db.Integer, db.ForeignKey('rstr.id'), nullable=True)

    def __repr__(self):
        if self.role == 'CUSTOMER':
            tmp = {
                'id': self.id,
                'username': self.username,
                'role': self.role
            }
            return '{id}: 用户 {username}, 类型 {role} '.format(**tmp)

        if self.role == 'BUSINESS':
            tmp = {
                'id': self.id,
                'username': self.username,
                'role': self.role,
                'authority': self.authority,
            }
            return '{id}: 用户 {username}, 类型 {role}, 权限 {authority} '.format(**tmp)

    def json(self):
        return {
            'id': self.id
        }

orders_dishes = db.Table('orders_dishes',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id'))
)

menu_dishes = db.Table('menu_dishes',
    db.Column('menu_id', db.Integer, db.ForeignKey('menu.id')),
    db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id'))
)

class Order(db.Model):

    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    tableId = db.Column(db.String(32), nullable=False)
    total = db.Column(db.Float, nullable=False)
    due = db.Column(db.Float, nullable=False)
    isPay = db.Column(db.Boolean, default=0, nullable=False)
    payWay = db.Column(db.String(32), nullable=False)
    payDate = db.Column(db.DateTime, nullable=False)

    dishes = db.relationship('Dish', secondary=orders_dishes, lazy='dynamic',
        backref=db.backref('orders', lazy='dynamic'))
    uid = db.Column(db.Integer, db.ForeignKey('users.id'),
        nullable=False)

    def __repr__(self):
        tmp = {
            'payDate': self.payDate.strftime("%Y-%m-%d %H:%M:%S"),
            'id': self.id,
            'tableId': self.tableId
        }
        return '{payDate}: 订单 {id}, 座位 {tableId} '.format(**tmp)

    def json(self):
        t_dishes = []
        for dish in self.dishes:
            t_dishes.append(dish.json())
        return {
            'id': self.id,
            'tableId': self.tableId,
            'total': self.total,
            'due': self.due,
            'isPay': self.isPay,
            'payWay': str(self.payWay),
            'payDate': self.payDate.strftime("%Y-%m-%d %H:%M:%S"),
            'dishes': t_dishes
        }

class Dish(db.Model):

    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    category = db.Column(db.String(32), nullable=False)
    img = db.Column(db.String(256), nullable=True)
    price = db.Column(db.Float, nullable=False)
    avaliable = db.Column(db.Boolean, default=0, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        tmp = {
            'id': self.id,
            'name': self.name,
            'price': self.price
        }
        return 'id: {id}, 菜名: {name}, 价格: {price} '.format(**tmp)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'img': self.img,
            'price': self.price,
            'avaliable': self.avaliable,
            'stock': self.stock,
            'likes': self.likes,
            'description': self.description
        }

class Menu(db.Model):

    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    dishes = db.relationship('Dish', secondary=menu_dishes, lazy='dynamic',
        backref=db.backref('menu', lazy='dynamic'))

    rstr_id = db.Column(db.Integer, db.ForeignKey('rstr.id'), nullable=False)

    def __repr__(self):
        tmp = {
            'id': self.id,
            'name': self.name,
        }
        return 'id: {id}, 菜单: {name}'.format(**tmp)

    def json(self):
        content = []
        category = {}
        for dish in self.dishes:
            if dish.category in category.keys():
                category[dish.category].append(dish.json())
            else:
                category[dish.category] = [dish.json()]

        for cat in category:
            content.append({'category':cat, 'dishes':category[cat]})
        return {
            'id': self.id,
            'name': self.name,
            'content': content
        }

class Rstr(db.Model):

    __tablename__ = 'rstr'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    info = db.Column(db.String(256), nullable=False)
    menus = db.relationship('Menu', backref='rstr', lazy='dynamic')
    cars = db.relationship('Carousel', backref='rstr', lazy='dynamic')

    def __repr__(self):
        tmp = {
            'id': self.id,
            'name': self.name,
            'info': self.info
        }
        return 'id: {id}, 餐馆: {name}, 说明: {info} '.format(**tmp)

    def json(self):
        menu = self.menus[0].json()
        tmpcars = []
        for car in self.cars:
            tmpcars.append(car.json())
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'carousel': tmpcars,
            'menu': menu
        }

class Carousel(db.Model):

    __tablename__ = 'carousel'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    info = db.Column(db.String(256), nullable=False)
    img = db.Column(db.String(256), nullable=False)

    rstr_id = db.Column(db.Integer, db.ForeignKey('rstr.id'), nullable=False)

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'info': self.info,
            'img': self.img
        }