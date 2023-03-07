from functools import wraps
from flask import Response

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from app.controllers.user import UserController


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            user = UserController.get_user_by_public_id(claims.get('sub',''))

            if user and user.is_admin:
                return fn(*args, **kwargs)
            else:
                return Response(status=403)

        return decorator

    return wrapper
