from functools import wraps
from flask import current_app, _request_ctx_stack, has_request_context
import flask_login
from flask_login import LoginManager
from werkzeug.local import LocalProxy
from app.models import User


login_manager = LoginManager()

current_user = LocalProxy(lambda: _get_user())

def login_required(authority="ANY"):
    """Custom login required decorator.
    If the method contains {userID_filed_name} args, the decorator would check whether
    the userId is the same as current user's.

    Args:
        authority (str, optional): {ANY, customer, manager, cook} The required role of the user
    Returns:
        function: The desired decorator wrapper.
    """
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return current_app.login_manager.unauthorized()
            if authority != "ANY":
                if authority == 'customer' and current_user.authority == 'cook':
                    return {'message': 'Your authority is not valid.'}, 401
                if authority == 'cook' and current_user.authority == 'customer':
                    return {'message': 'Your authority is not valid.'}, 401
                if authority == 'manager' and current_user.authority == 'manager':
                    return {'message': 'Your authority is not valid.'}, 401

            return func(*args, **kwargs)
        return decorated_view
    return wrapper

def _get_user():
    if has_request_context() and not hasattr(_request_ctx_stack.top, 'user'):
        current_app.login_manager._load_user()

    return getattr(_request_ctx_stack.top, 'user', None)

def init_app(app):
   login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

@login_manager.unauthorized_handler
def unauthorized_callback():
    return {'message': 'Login required.'}, 401