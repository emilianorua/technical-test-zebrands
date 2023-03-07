import uuid
from pydantic import validate_email
from app.repositories.auth import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import Unauthorized
from flask_jwt_extended import create_access_token
from app.structures.auth import AuthData
from app.structures.user import UserData


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
    def get_access_token(cls, username: str, password: str) -> str:
        user = AuthData(
            username=username,
            password=password
        )

        user = UserRepository.get_user_by_username(username)

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            return access_token

        raise Unauthorized()

    @classmethod
    def get_user_by_username(cls, username: str) -> UserData:

        user = UserRepository.get_user_by_username(username)

        return user
