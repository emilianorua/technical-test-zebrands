from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity
from pydantic import EmailError, ValidationError
from app.controllers.user import DeleteOwnUser, UserAlreadyExists, UserController
from app.utils.decorators import admin_required


bp_users = Blueprint('users', __name__, url_prefix='/users')


@bp_users.route('/')
@admin_required()
def get_all():
    users = UserController.get_all()
    users_list = [user.dict(exclude={'password'}) for user in users]
    return jsonify(users_list)


@bp_users.route('/', methods=['POST'])
@admin_required()
def create_user():
    data = request.get_json()

    try:
        user = UserController.create_user(
            username=data.get('username', None),
            password=data.get('password', None),
            email=data.get('email', None),
            is_admin=data.get('is_admin', None)
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


@bp_users.route('/<id>', methods=['PUT'])
@admin_required()
def update_user(id):
    data = request.get_json()

    try:
        user = UserController.update_user(
            public_id=id,
            username=data.get('username', None),
            password=data.get('password', None),
            email=data.get('email', None),
            is_admin=data.get('is_admin', None)
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


@bp_users.route('/<id>', methods=['DELETE'])
@admin_required()
def delete_user(id):
    current_public_id = get_jwt_identity()

    try:
        UserController.delete_user(current_public_id, id)
    except DeleteOwnUser as e:
        return jsonify({"msg": str(e)}), 403
    except Exception:
        return Response(status=500)

    return Response(status=200)
