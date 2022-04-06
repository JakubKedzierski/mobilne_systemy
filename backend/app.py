from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_session import Session
import secrets
import os

db = SQLAlchemy()
migrate = Migrate()

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = "filesystem"
    SESSION_PERMANENT = False
    SECRET_KEY = secrets.token_hex(16)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    Session(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from backend.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


if __name__ == "__main__":
    app = create_app()

