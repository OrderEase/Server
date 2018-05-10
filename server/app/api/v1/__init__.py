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
from .dishes import api as dishes_api
from .order import api as order_api
from .pay import api as pay_api
from .rstr import api as rstr_api

myapi.add_namespace(buser_api, path='/api/buser')
myapi.add_namespace(cuser_api, path='/api/cuser')
myapi.add_namespace(dish_api, path='/api/dish')
myapi.add_namespace(dishes_api, path='/api/dishes')
myapi.add_namespace(order_api, path='/api/order')
myapi.add_namespace(pay_api, path='/api/pay')
myapi.add_namespace(rstr_api, path='/api/rstr')