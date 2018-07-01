# modify your own config
import os

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # important
    PERMANENT_SESSION_LIFETIME = 3600 * 24 * 5

    basedir = os.path.abspath(os.path.dirname(__file__))
    rootdir = os.path.abspath(os.path.dirname(basedir))
    UPLOADED_DISHES_DEST = os.path.join(rootdir, 'static/images/dishes')
    UPLOADED_RESTRTS_DEST = os.path.join(rootdir, 'static/images/restrts')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRODUCTION_DATABASE_URI", '')
    SECRET_KEY = os.environ.get("SECRET_KEY", "Sdna2MshdG39DOA2skajd")

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ("DEVELOPMENT_DATABASE_URI", '')
    SECRET_KEY = os.environ.get("SECRET_KEY", "Sdna2MshdG39DOA2skajd")

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get("TEST_DATABASE_URI", '')
    SECRET_KEY = "Sdna2MshdG39DOA2skajd"
    TESTING = True

config = {
    'PRODUCTION': ProductionConfig,
    'DEVELOPMENT': DevelopmentConfig,
    'TEST': TestingConfig
}




