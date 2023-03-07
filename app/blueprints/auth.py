from flask import Response, jsonify, request
from flask import Blueprint
from pydantic import EmailError, ValidationError
from app.controllers.auth import AuthController
from werkzeug.exceptions import Unauthorized
from app.controllers.user import UserController, UserAlreadyExists

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.route('/register',  methods=['POST'])
def register():
    data = request.get_json()

    try:
        user = UserController.create_user(
            username=data.get('username', None),
            password=data.get('password', None),
            email=data.get('email', None),
            is_admin=False
        )
    except (ValidationError, AttributeError):
        return jsonify({"msg": "must complete all fields correctly"}), 400
    except EmailError:
        return jsonify({"msg": "please insert a valid email address"}), 400
    except UserAlreadyExists as e:
        return jsonify({"msg": str(e)}), 400
    except Exception:
        return Response(status=500)

    return jsonify(user.dict(exclude={'password'}))


@bp_auth.route('/login',  methods=['POST'])
def login():
    data = request.get_json()

    try:
        access_token = AuthController.get_access_token(
            username=data.get('username', ''),
            password=data.get('password', '')
        )
    except (ValidationError, AttributeError):
        return jsonify({"msg": "must complete all fields correctly"}), 400
    except Unauthorized:
        return jsonify({"msg": "invalid username or password"}), 401
    except Exception:
        return Response(status=500)

    if access_token:
        return jsonify({'access_token': access_token})

    return jsonify({"msg": "invalid username or password"}), 401
