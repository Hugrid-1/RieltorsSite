#подгрузка необходимых библиотек
from flask_login import UserMixin
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import relationship

from sweater import db #подгрузка обьекта базы данных

class User(db.Model, UserMixin): #модель таблицы Users
    id = db.Column(db.Integer,primary_key=True)
    login = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    realty = relationship('Realty', backref='User', uselist=False) #определение связи с таблицей Realtys
    sale = relationship('Sale', backref='User', uselist=False) #определение связи с таблицей Sale

class Realty(db.Model): #модель таблицы Realtys
    id = db.Column(db.Integer,primary_key=True)
    owner_id = db.Column(db.Integer,ForeignKey('user.id')) #определение внешнего ключа Users
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    area = db.Column(db.Float, nullable=False)
    roomCount = db.Column(db.Integer, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    is_for_sale = db.Column(db.Boolean)
    sale = relationship('Sale', backref='Realty', uselist=False) #определение связи с таблицей Sale


class Sale(db.Model): #модель таблицы Sales
    id = db.Column(db.Integer, primary_key=True)
    buyer_id  = db.Column(db.Integer, ForeignKey('user.id')) #определение внешнего ключа Users
    realty_id = db.Column(db.Integer, ForeignKey('realty.id')) #определение внешнего ключа из таблицы Realtys
    date_sale = db.Column(db.Date(), nullable=False)


