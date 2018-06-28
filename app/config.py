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
    GEN_FAKE_DATA = False
    SQLALCHEMY_DATABASE_URI = os.environ["PRODUCTION_DATABASE_URI"]
    SECRET_KEY = os.environ["SECRET_KEY"]

class DevelopmentConfig(Config):
    GEN_FAKE_DATA = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ["DEVELOPMENT_DATABASE_URI"]
    SECRET_KEY = os.environ["SECRET_KEY"]

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ["TEST_DATABASE_URI"]
    SECRET_KEY = "Sdna2MshdG39DOA2skajd"
    GEN_FAKE_DATA = True
    TESTING = True

config = {
    'Production': ProductionConfig,
    'Development': DevelopmentConfig,
    'Test': TestingConfig
}



