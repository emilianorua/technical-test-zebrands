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
    def get_user_by_public_id(cls, public_id: str) -> UserData:

        user = User.query.filter_by(public_id=public_id).one_or_none()

        if not user:
            return None

        user_data = UserData.from_orm(user)

        return user_data

    @classmethod
    def username_exists(cls, username: str, public_id: str = None) -> bool:

        user = User.query.filter(
            User.username == username,
            User.public_id != public_id
        ).one_or_none()

        return True if user else False

    @classmethod
    def email_exists(cls, email: str, public_id: str = None) -> bool:

        user = User.query.filter(
            User.email == email,
            User.public_id != public_id
        ).one_or_none()

        return True if user else False

    @classmethod
    def get_all(cls):

        users = db.session.query(User).all()
        users_list = [UserData.from_orm(user) for user in users]
        return users_list

    @classmethod
    def update_user(cls, user: UserData) -> UserData:
        user_to_update = User.query.filter_by(public_id=user.public_id).first()

        if user:
            user_to_update.username = user.username
            user_to_update.password = user.password
            user_to_update.email = user.email
            user_to_update.role = user.role

        db.session.commit()

        return user

    @classmethod
    def delete_user(cls, public_id: str):
        user_to_delete = User.query.filter_by(public_id=public_id).first()

        db.session.delete(user_to_delete)
        db.session.commit()
