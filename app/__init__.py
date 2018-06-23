from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from app.models import db
from datetime import datetime

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.app = app
    db.init_app(app)
    db.create_all()

    from app import login
    login.init_app(app)

    from app.api.v1 import myapi
    myapi.init_app(app)

    # create a restaurant
    from app.models import Restaurant
    restaurant = Restaurant.query.filter_by(id=1).first()
    if restaurant is None:
        restaurant = Restaurant()
        restaurant.id = 1
        restaurant.open = datetime.strptime('00:00:00', "%H:%M:%S")
        restaurant.close = datetime.strptime('00:00:00', "%H:%M:%S")        
        restaurant.name = 'default'
        db.session.add(restaurant)
        db.session.commit()

    # add 3 default carousels
    from app.models import Carousel
    car = Carousel.query.filter_by(restId=1).first()
    if car is None:
        for i in range(1, 4):
            car = Carousel()
            car.id = i
            car.name = 'default'
            car.info = 'default'
            car.img = 'https://raw.githubusercontent.com/OrderEase/Server/master/assets/default.png'
            car.restId = 1
            db.session.add(car)
            db.session.commit()

    # create fake restaurant
    restaurant = Restaurant.query.filter_by(id=-1).first()
    if restaurant is None:
        restaurant = Restaurant()
        restaurant.id = -1
        restaurant.name = 'fake'
        db.session.add(restaurant)
        db.session.commit()

    # create fake menu
    from app.models import Menu
    menu = Menu.query.filter_by(id=-1).first()
    if menu is None:
        menu = Menu()
        menu.id = -1
        menu.name = 'fake'
        menu.used = 0
        menu.delete = True
        menu.restId = -1
        db.session.add(menu)
        db.session.commit()

    # create fake category
    from app.models import Category
    category = Category.query.filter_by(id=-1).first()
    if category is None:
        category = Category()
        category.rank = -1
        category.id = -1
        category.name = 'fake'
        category.delete = True
        category.menuId = -1
        db.session.add(category)
        db.session.commit()

    return app
