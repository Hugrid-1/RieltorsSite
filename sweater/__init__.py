from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_string = "postgresql://vova:123@localhost/RieltorsSite" #адрес подключения к БД
dbEngine = create_engine(db_string) #создание класса базы данных

UPLOAD_FOLDER = 'sweater\\static\\images'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask( __name__ )
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = db_string #опредления встроенного в Flask базы данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # определение папки для
app.config['UPLOADS_DEFAULT_DEST'] = UPLOAD_FOLDER
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
manager = LoginManager(app)
Session = sessionmaker(db)
session = Session()

from sweater import models,routes

db.create_all()
db.session.commit()


