import uuid
from pydantic import validate_email
from app.repositories.product import ProductRepository
from app.repositories.user import UserRepository
from app.structures.product import ProductData
from werkzeug.security import generate_password_hash

from app.structures.user import Roles


class ProductAlreadyExists(Exception):
    pass


class ProductController():

    @classmethod
    def create_product(cls, name: str, sku: str, price: float, brand: str, queries: int) -> ProductData:

        product = ProductData(
            public_id=str(uuid.uuid4()),
            name=name,
            sku=sku,
            price=price,
            brand=brand,
            queries=queries
        )

        if ProductRepository.name_exists(name):
            raise ProductAlreadyExists('the product name is already in use')

        if ProductRepository.sku_exists(sku):
            raise ProductAlreadyExists('the sku is already in use')

        ProductRepository.create_product(product)

        return product

    @classmethod
    def update_product(cls, public_id: str, name: str, sku: str, price: float, brand: str, queries: int) -> ProductData:

        product = ProductData(
            public_id=public_id,
            name=name,
            sku=sku,
            price=price,
            brand=brand,
            queries=queries
        )

        if ProductRepository.name_exists(name, public_id):
            raise ProductAlreadyExists('the product name is already in use')

        if ProductRepository.sku_exists(sku, public_id):
            raise ProductAlreadyExists('the email is already in use')

        ProductRepository.update_product(product)

        return product

    @classmethod
    def get_product_by_public_id(cls, public_id: str) -> ProductData:

        product = ProductRepository.get_product_by_public_id(public_id)

        return product

    @classmethod
    def get_all(cls, public_id: str):

        products = ProductRepository.get_all(public_id=public_id)

        return products

    @classmethod
    def delete_product(cls, public_id: str):

        ProductRepository.delete_product(public_id)

    @classmethod
    def increment_queries(cls, public_id: str, user_public_id: str = None):

        user = UserRepository.get_user_by_public_id(user_public_id)

        if (user and user.role == Roles.USER) or not user:
            ProductRepository.increment_queries(public_id)
