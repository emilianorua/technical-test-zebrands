import uuid
from app.repositories.product import ProductRepository
from app.repositories.user import UserRepository
from app.structures.product import ProductData
from app.structures.user import Roles
from app.utils.email_helper import EmailHelper


class ProductAlreadyExists(Exception):
    pass


class ProductNotFound(Exception):
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
    def update_product(cls, user_public_id: str, public_id: str, name: str, sku: str, price: float, brand: str) -> ProductData:

        old_product = ProductController.get_product_by_public_id(public_id)

        if not old_product:
            raise ProductNotFound()

        product = ProductData(
            public_id=public_id,
            name=name,
            sku=sku,
            price=price,
            brand=brand,
            queries=old_product.queries
        )

        if ProductRepository.name_exists(name, public_id):
            raise ProductAlreadyExists('the product name is already in use')

        if ProductRepository.sku_exists(sku, public_id):
            raise ProductAlreadyExists('the email is already in use')

        ProductRepository.update_product(product)

        email_text = cls.get_email_text(user_public_id, old_product, product)
        EmailHelper.send_email(
            f'Updated product: {old_product.name}',
            email_text,
            to_admins=True,
            user_public_id=user_public_id
        )        

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

        product = ProductController.get_product_by_public_id(public_id)

        if not product:
            raise ProductNotFound()

        ProductRepository.delete_product(public_id)

    @classmethod
    def increment_queries(cls, public_id: str, user_public_id: str = None):

        user = UserRepository.get_user_by_public_id(user_public_id)

        if (user and user.role == Roles.USER) or not user:
            ProductRepository.increment_queries(public_id)

    @classmethod
    def get_email_text(cls, user_public_id: str, old_product: ProductData, new_product: ProductData) -> str:
        user = UserRepository.get_user_by_public_id(user_public_id)

        email_text = f'The user {user.username} has updated the following values of the product {old_product.name}:\r'

        old_product_dict = old_product.dict()
        new_product_dict = new_product.dict()

        for key in old_product_dict:
            if key == 'queries':
                continue
            if old_product_dict.get(key) != new_product_dict.get(key):
                email_text += f'{key}: {old_product_dict.get(key)} -> {new_product_dict.get(key)}\r'

        return email_text
