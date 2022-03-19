from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask import Flask


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def hello_world():
        return "Hello World"

    return app


if __name__ == "__main__":
    app = create_app()

