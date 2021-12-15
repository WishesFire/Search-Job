"""
This package contains modules defining urls
"""

from .views.main import base_view
from .views.vacancies import vacancies_view
from .views.user import auth_view
from .views.error import error_view

from .rest.main_api import TestConnection


def register_handlers(app):
    """
    Register views
    """
    app.register_blueprint(base_view, url_prefix="/")
    app.register_blueprint(vacancies_view, url_prefix="/")
    app.register_blueprint(auth_view, url_prefix="/")
    app.register_blueprint(error_view)


def register_api_handlers(api):
    api.add_resource(TestConnection, "/ping")
