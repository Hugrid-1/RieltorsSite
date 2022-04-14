from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, configure_uploads, IMAGES

UPLOAD_FOLDER = 'sweater\\static\\images'
# расширения файлов, которые разрешено загружать
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask( __name__ )
app.secret_key = 'some secret salt'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vova:123@localhost/RieltorsSite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOADS_DEFAULT_DEST'] = UPLOAD_FOLDER
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
manager = LoginManager(app)

from sweater import models,routes

db.create_all()
db.session.commit()


