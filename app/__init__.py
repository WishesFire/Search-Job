"""
Sources root package.

Initializes web application and web service, contains following subpackages and
modules:

Subpackages:
- `migrations`: contains migration files used to manage database schema
- `models`: contains modules with Python classes describing database models
- `rest`: contains modules with RESTful service implementation
- `service`: contains modules with classes used to work with database
- `static`: contains web application static files (scripts, styles, images)
- `templates`: contains web application html templates
- `views`: contains modules with web views
- `tests`: contains tests
- `configs`: contains modules with configs
- `routes.py`: defines model representing urls
"""
# pylint: disable=wrong-import-position
from flask import Flask
from .configs.config import TestBaseConfig
from sqlalchemy_utils import database_exists, create_database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Logging


def create_app():
    """
    Create instance web application
    """
    app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
    app.config.from_object("app.configs.config.TestBaseConfig")

    # Database
    db.init_app(app)
    migrate.init_app(app, db)

    # Login users
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from app.models.model import Category, Vacancy, User
    from app.routes import register_handlers

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    if not database_exists(TestBaseConfig.SQLALCHEMY_DATABASE_URI):
        create_database(TestBaseConfig.SQLALCHEMY_DATABASE_URI)
        with app.app_context():
            db.create_all()

        from .models.handlers import init_start_categories
        init_start_categories(app)

    register_handlers(app)

    return app
