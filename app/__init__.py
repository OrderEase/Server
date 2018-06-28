from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads
from flask_cors import CORS
from app.models import db
from app.config import config
from datetime import datetime

restrts_upload_set = UploadSet('restrts')
dishes_upload_set = UploadSet('dishes')

def create_app(config_name):

    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)

    app.config.from_object(config[config_name])

    configure_uploads(app, (restrts_upload_set, dishes_upload_set))

    db.app = app
    db.init_app(app)
    db.create_all()

    from app import login
    login.init_app(app)

    from app.api.v1 import myapi
    myapi.init_app(app)

    return app
