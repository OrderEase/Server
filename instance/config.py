# modify your own config
import os
basedir = os.path.abspath(os.path.dirname(__file__))
rootdir = os.path.abspath(os.path.dirname(basedir))

SQLALCHEMY_DATABASE_URI="mysql://root:@localhost:3306/test?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS=True
SECRET_KEY = 'Sdna2MshdG39DOA2skajd'

UPLOADED_DISHES_DEST = os.path.join(rootdir, 'static/images/dishes')
UPLOADED_RESTRTS_DEST = os.path.join(rootdir, 'static/images/restrts')