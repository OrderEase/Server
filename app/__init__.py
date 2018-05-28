from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from app.models import db


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

    # create a rstr
    from app.models import Rstr
    rstr = Rstr.query.filter_by(id=1).first()
    if rstr is None:
        rstr = Rstr()
        rstr.id = 1
        rstr.name = 'default'
        rstr.info = 'default'
        db.session.add(rstr)
        db.session.commit()

    # add 3 default carousels
    from app.models import Carousel
    car = Carousel.query.filter_by(rstr_id=1).first()
    if car is None:
        for i in range(1, 4):
            car = Carousel()
            car.id = i
            car.name = 'default'
            car.info = 'default'
            car.img = 'https://raw.githubusercontent.com/OrderEase/Server/master/assets/default.png'
            car.rstr_id = 1
            db.session.add(car)
            db.session.commit()

    return app
