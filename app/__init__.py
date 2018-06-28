from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads
from flask_cors import CORS
from app.models import db
from datetime import datetime

restrts_upload_set = UploadSet('restrts')
dishes_upload_set = UploadSet('dishes')

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    configure_uploads(app, (restrts_upload_set, dishes_upload_set))

    db.app = app
    db.init_app(app)
    db.create_all()

    from app import login
    login.init_app(app)

    from app.api.v1 import myapi
    myapi.init_app(app)

    return app
