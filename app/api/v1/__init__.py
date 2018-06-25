from flask_restplus import Api

myapi = Api(
	title='OrderEase',
	version='0.1',
	catch_all_404s=True,
	serve_challenge_on_401=True
)

from .buser import api as buser_api
from .cuser import api as cuser_api
from .menu import api as menu_api
from .order import api as order_api
from .restrt import api as restrt_api
from .rule import api as rule_api
from .promotion import api as promotion_api
from .photo import api as photo_api

myapi.add_namespace(buser_api, path='/api/busers')
myapi.add_namespace(cuser_api, path='/api/cusers')
myapi.add_namespace(menu_api, path='/api/menus')
myapi.add_namespace(order_api, path='/api/orders')
myapi.add_namespace(restrt_api, path='/api/restrt')
myapi.add_namespace(promotion_api, path='/api/promotions')
myapi.add_namespace(photo_api, path='/api/photos')
