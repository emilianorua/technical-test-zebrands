from app.repositories.user import UserRepository
from werkzeug.security import check_password_hash
from werkzeug.exceptions import Unauthorized
from flask_jwt_extended import create_access_token
from app.structures.auth import AuthData


class AuthController():

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
