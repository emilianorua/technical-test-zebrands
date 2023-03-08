from flask import Blueprint, Response, jsonify, request
from pydantic import ValidationError
from app.controllers.product import ProductAlreadyExists, ProductController
from app.utils.decorators import admin_required


bp_products = Blueprint('products', __name__, url_prefix='/products')


@bp_products.route('/')
@admin_required()
def get_all():
    products = ProductController.get_all()
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
            brand=data.get('brand', None)
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

    try:
        product = ProductController.update_product(
            public_id=id,
            name=data.get('name', None),
            sku=data.get('sku', None),
            price=data.get('price', None),
            brand=data.get('brand', None)
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
    try:
        ProductController.delete_product(id)
    except Exception:
        return Response(status=500)

    return Response(status=200)
