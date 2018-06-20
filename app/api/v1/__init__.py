from flask_restplus import Api

myapi = Api(
	title='OrderEase',
	version='0.1',
	catch_all_404s=True,
	serve_challenge_on_401=True
)

from .buser import api as buser_api
from .cuser import api as cuser_api
from .dish import api as dish_api
from .order import api as order_api
from .rstr import api as rstr_api
from .rule import api as rule_api
from .promotion import api as promotion_api

myapi.add_namespace(buser_api, path='/api/busers')
myapi.add_namespace(cuser_api, path='/api/cusers')
myapi.add_namespace(dish_api, path='/api/dish')
myapi.add_namespace(order_api, path='/api/order')
myapi.add_namespace(rstr_api, path='/api/rstr')
myapi.add_namespace(promotion_api, path='/api/promotions')
