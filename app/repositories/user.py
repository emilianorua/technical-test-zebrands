from app.models.user import User
from app.db import db
from app.structures.user import UserData


class UserRepository():

    @classmethod
    def create_user(cls, user: UserData) -> UserData:
        new_user = User(
            **user.dict()
        )

        db.session.add(new_user)
        db.session.commit()

        return user

    @classmethod
    def get_user_by_username(cls, username: str) -> UserData:

        user = User.query.filter_by(username=username).one_or_none()

        if not user:
            return None

        user_data = UserData.from_orm(user)

        return user_data

    @classmethod
    def username_exists(cls, username: str) -> bool:

        user = User.query.filter_by(username=username).one_or_none()

        return True if user else False

    @classmethod
    def email_exists(cls, email: str) -> bool:

        user = User.query.filter_by(email=email).one_or_none()

        return True if user else False
