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
import logging
from flask import Flask, Blueprint
from app.configs.config import TestBaseConfig
from .configs.config import TestBaseConfig
from sqlalchemy_utils import database_exists, create_database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_admin import Admin


# Init elements
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
ma = Marshmallow()
jwt = JWTManager()
mail = Mail()
admin = Admin(name='jobs', template_mode='bootstrap3')

# Logging
if TestBaseConfig.LOGGING:
    logging.basicConfig(filename="record.log", level=logging.INFO, filemode="w",
                        format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def create_app():
    """
    Create instance web application
    """
    app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
    app.config.from_object("app.configs.config.TestBaseConfig")

    # API
    api_bp = Blueprint("api", __name__)
    api = Api(api_bp)
    ma.init_app(app)
    jwt.init_app(app)

    # Database
    db.init_app(app)
    migrate.init_app(app, db)

    # Login users
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = 'auth.login'

    # Mail
    mail.init_app(app)

    from app.models.model import Category, Vacancy, User
    from app.routes import register_handlers, register_api_handlers
    from app.views.user import JobAdminModelView

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # First run
    if not database_exists(TestBaseConfig.SQLALCHEMY_DATABASE_URI):
        create_database(TestBaseConfig.SQLALCHEMY_DATABASE_URI)
        with app.app_context():
            db.create_all()

        from .models.handlers import init_start_categories, init_admin_user
        init_start_categories(app)
        init_admin_user(app)

    # Registration handlers
    register_handlers(app)
    register_api_handlers(api)

    # Admin panel
    admin.init_app(app)
    admin.add_view(JobAdminModelView(Category, db.session))
    admin.add_view(JobAdminModelView(Vacancy, db.session))
    admin.add_view(JobAdminModelView(User, db.session))

    csrf.exempt(api_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
