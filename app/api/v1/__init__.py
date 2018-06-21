from flask_restplus import Api

myapi = Api(
	title='OrderEase',
	version='0.1',
	catch_all_404s=True,
	serve_challenge_on_401=True
)

from .buser import api as buser_api
from .cuser import api as cuser_api
from .menus import api as menus_api
from .order import api as order_api
from .restrt import api as restrt_api

myapi.add_namespace(buser_api, path='/api/buser')
myapi.add_namespace(cuser_api, path='/api/cuser')
myapi.add_namespace(menus_api, path='/api/menus')
myapi.add_namespace(order_api, path='/api/orders')
myapi.add_namespace(restrt_api, path='/api/restrt')
