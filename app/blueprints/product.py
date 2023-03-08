from flask import Blueprint, Response, jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from pydantic import ValidationError
from app.controllers.product import ProductAlreadyExists, ProductController
from app.utils.decorators import admin_required


bp_products = Blueprint('products', __name__, url_prefix='/products')


@bp_products.route('/', defaults={'public_id': None})
@bp_products.route('/<public_id>')
def get_all(public_id):

    current_public_id = None

    if verify_jwt_in_request(optional=True):
        current_public_id = get_jwt_identity()

    if public_id:
        ProductController.increment_queries(
            public_id=public_id,
            user_public_id=current_public_id
        )

    products = ProductController.get_all(public_id)
    products_list = [product.dict() for product in products]
    return jsonify(products_list)


@bp_products.route('/', methods=['POST'])
@admin_required()
def create_product():
    data = request.get_json()

    try:
        product = ProductController.create_product(
            name=data.get('name', None),
            sku=data.get('sku', None),
            price=data.get('price', None),
            brand=data.get('brand', None),
            queries=0
        )
    except (ValidationError, AttributeError):
        return jsonify({"msg": "must complete all fields correctly"}), 400
    except ProductAlreadyExists as e:
        return jsonify({"msg": str(e)}), 400
    except Exception as e:
        print(e)
        return Response(status=500)

    return jsonify(product.dict(exclude={'password'}))


@bp_products.route('/<id>', methods=['PUT'])
@admin_required()
def update_product(id):
    data = request.get_json()

    product = ProductController.get_product_by_public_id(id)

    if not product:
        return Response(status=404)

    try:
        product = ProductController.update_product(
            public_id=id,
            name=data.get('name', None),
            sku=data.get('sku', None),
            price=data.get('price', None),
            brand=data.get('brand', None),
            queries=data.get('queries', None)
        )
    except (ValidationError, AttributeError):
        return jsonify({"msg": "must complete all fields correctly"}), 400
    except ProductAlreadyExists as e:
        return jsonify({"msg": str(e)}), 400
    except Exception:
        return Response(status=500)

    return jsonify(product.dict(exclude={'password'}))


@bp_products.route('/<id>', methods=['DELETE'])
@admin_required()
def delete_product(id):

    product = ProductController.get_product_by_public_id(id)

    if not product:
        return Response(status=404)

    try:
        ProductController.delete_product(id)
    except Exception:
        return Response(status=500)

    return Response(status=200)
