from functools import wraps
from flask import Response

from flask_jwt_extended import get_jwt, verify_jwt_in_request

from app.controllers.user import UserController
from app.structures.user import Roles


def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            
            user = UserController.get_user_by_public_id(claims.get('sub',''))

            if user and user.role == Roles.ADMIN:
                return fn(*args, **kwargs)
            else:
                return Response(status=403)

        return decorator

    return wrapper
