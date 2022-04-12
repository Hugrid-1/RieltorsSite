from flask_login import UserMixin

from sweater import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    login = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)