from flask_login import UserMixin

from sweater import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    login = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

class Realty(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    roomCount = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
