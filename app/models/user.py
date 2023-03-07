from sqlalchemy.sql import func
from sqlalchemy_serializer import SerializerMixin
from app.db import db
from app.structures.user import UserData


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'{self.username} ({self.email})'
