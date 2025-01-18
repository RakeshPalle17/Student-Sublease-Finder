from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_uploads import UploadSet, configure_uploads, IMAGES

db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sublease.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this in production
    app.config['UPLOADED_PHOTOS_DEST'] = 'uploads/photos'

    db.init_app(app)
    jwt = JWTManager(app)
    configure_uploads(app, photos)

    return app

