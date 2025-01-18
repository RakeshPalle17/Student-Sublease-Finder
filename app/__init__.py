from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Register blueprints
    from app.routes import auth_bp
    from app.auth import auth_user

    app.register_blueprint(auth_user, url_prefix='/auth')
    app.register_blueprint(auth_bp,  url_prefix='/bp')

    return app
