from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

orders_dishes = db.Table('orders_dishes',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('dish_id', db.Integer, db.ForeignKey('dish.id'), primary_key=True)
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
    uid = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)

    def __repr__(self):
        tmp = {
            'payDate': self.payDate.strftime("%Y-%m-%d %H:%M:%S"),
            'id': self.id,
            'tableId': self.tableId
        }
        return '{payDate}: 订单 {id}, 座位 {tableId} '.format(**tmp)

    def json(self):
        return {
            'id': self.id,
            'tableId': self.tableId,
            'total': self.total,
            'due': self.due,
            'isPay': self.isPay,
            'payWay': str(self.payWay),
            'payDate': self.payDate.strftime("%Y-%m-%d %H:%M:%S")
        }

class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    category = db.Column(db.String(32), nullable=False)
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
            'price': self.price,
            'avaliable': str(self.avaliable),
            'stock': self.stock,
            'likes': self.likes,
            'description': self.description
        }