from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
    app.config.from_object("app.configs.config.TestBaseConfig")
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user):
        return User.query.get(user)

    from app.models.model import Category, Vacancy, User
    from app.routes import register_handlers

    register_handlers(app)

    return app
