# coding=utf-8
from functools import wraps

from flask import g

from app.api_1_0.errors import forbidden


def permission_required(permission):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('没有该权限')
            return func(*args, **kwargs)
        return decorated_function
    return decorator