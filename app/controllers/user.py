import uuid
from pydantic import validate_email
from app.repositories.user import UserRepository
from app.structures.user import UserData
from werkzeug.security import generate_password_hash


class UserAlreadyExists(Exception):
    pass


class DeleteOwnUser(Exception):
    pass


class UserController():

    @classmethod
    def create_user(cls, username: str, password: str, email: str, role: str) -> UserData:
        validate_email(email)

        user = UserData(
            public_id=str(uuid.uuid4()),
            username=username,
            password=password,
            email=email,
            role=role
        )

        if UserRepository.username_exists(username):
            raise UserAlreadyExists('the username is already in use')

        if UserRepository.email_exists(email):
            raise UserAlreadyExists('the email is already in use')

        user.password = generate_password_hash(password, method='sha256')

        UserRepository.create_user(user)

        return user

    @classmethod
    def update_user(cls, public_id: str, username: str, password: str, email: str, role: int) -> UserData:
        validate_email(email)

        user = UserData(
            public_id=public_id,
            username=username,
            password=password,
            email=email,
            role=role
        )

        if UserRepository.username_exists(username, public_id):
            raise UserAlreadyExists('the username is already in use')

        if UserRepository.email_exists(email, public_id):
            raise UserAlreadyExists('the email is already in use')

        user.password = generate_password_hash(password, method='sha256')

        UserRepository.update_user(user)

        return user

    @classmethod
    def get_user_by_username(cls, username: str) -> UserData:

        user = UserRepository.get_user_by_username(username)

        return user

    @classmethod
    def get_user_by_public_id(cls, public_id: str) -> UserData:

        user = UserRepository.get_user_by_public_id(public_id)

        return user

    @classmethod
    def get_all(cls):

        users = UserRepository.get_all()

        return users

    @classmethod
    def delete_user(cls, current_public_id: str, public_id: str):
        if current_public_id == public_id:
            raise DeleteOwnUser('can\'t delete own user')

        UserRepository.delete_user(public_id)
