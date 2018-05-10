from flask import Flask, request


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    from app.api.v1 import myapi
    myapi.init_app(app)

    return app
