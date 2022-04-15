from flask_login import UserMixin
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sweater import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    login = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    realty = relationship('Realty', backref='User', uselist=False)

class Realty(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    owner_id = db.Column(db.Integer,ForeignKey('user.id'))
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    roomCount = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    is_for_sale = db.Column(db.Boolean)
    sale = relationship('Sale', backref='Realty', uselist=False)


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    realty_id = db.Column(db.Integer, ForeignKey('realty.id'))
    date_sale = db.Column(db.Date(), nullable=False)

