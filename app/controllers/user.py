import uuid
from pydantic import validate_email
from app.repositories.user import UserRepository
from app.structures.user import UserData
from werkzeug.security import generate_password_hash


class UserAlreadyExists(Exception):
    pass


class UserController():

    @classmethod
    def create_user(cls, username: str, password: str, email: str, is_admin: bool) -> UserData:
        validate_email(email)

        user = UserData(
            public_id=str(uuid.uuid4()),
            username=username,
            password=password,
            email=email,
            is_admin=is_admin
        )

        if UserRepository.username_exists(username):
            raise UserAlreadyExists('the username is already in use')

        if UserRepository.email_exists(email):
            raise UserAlreadyExists('the email is already in use')

        user.password = generate_password_hash(password, method='sha256')

        UserRepository.create_user(user)

        return user

    @classmethod
    def get_user_by_username(cls, username: str) -> UserData:

        user = UserRepository.get_user_by_username(username)

        return user
