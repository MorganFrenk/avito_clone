from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    avito_id = db.Column(db.String, unique=True)
    name = db.Column(db.String, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    link_photo = db.Column(db.String, nullable=False)
    price = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=True)
    address = db.Column(db.Text, nullable=True)
    category = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Item {self.name} {self.id}>'
