from sqlalchemy.sql import func
from app.db import db


class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    brand = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'{self.name} ({self.brand})'
