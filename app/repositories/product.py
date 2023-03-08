from sqlalchemy import or_
from app.models.product import Product
from app.structures.product import ProductData
from app.db import db


class ProductRepository():

    @classmethod
    def create_product(cls, product: ProductData) -> ProductData:
        new_product = Product(
            **product.dict()
        )

        db.session.add(new_product)
        db.session.commit()

        return product

    @classmethod
    def get_product_by_public_id(cls, public_id: str) -> ProductData:

        product = Product.query.filter_by(public_id=public_id).one_or_none()

        if not product:
            return None

        product_data = ProductData.from_orm(product)

        return product_data

    @classmethod
    def name_exists(cls, name: str, public_id: str = None) -> bool:

        product = Product.query.filter(
            Product.name == name,
            Product.public_id != public_id
        ).one_or_none()

        return True if product else False

    @classmethod
    def sku_exists(cls, sku: str, public_id: str = None) -> bool:

        product = Product.query.filter(
            Product.sku == sku,
            Product.public_id != public_id
        ).one_or_none()

        return True if product else False

    @classmethod
    def get_all(cls, public_id: str):

        products = db.session.query(Product).filter(
            or_(Product.public_id == public_id, False if public_id else True)
        ).all()

        products_list = [ProductData.from_orm(product) for product in products]
        return products_list

    @classmethod
    def update_product(cls, product: ProductData) -> ProductData:

        product_to_update = Product.query.filter_by(
            public_id=product.public_id).first()

        if product:
            product_to_update.name = product.name
            product_to_update.sku = product.sku
            product_to_update.price = product.price
            product_to_update.brand = product.brand

        db.session.commit()

        return product

    @classmethod
    def delete_product(cls, public_id: str):
        product_to_delete = Product.query.filter_by(
            public_id=public_id).first()

        db.session.delete(product_to_delete)
        db.session.commit()
