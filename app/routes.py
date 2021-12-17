"""
This package contains modules defining urls
"""

from .views.main import base_view
from .views.vacancies import vacancies_view
from .views.user import auth_view
from .views.error import error_view

from .rest.main_api import TestConnection
from .rest.categories_api import CategoryAPI
from .rest.vacancies_api import VacancyAPI
from .rest.user_api import LoginUserAPI, RegistrationUserAPI


def register_handlers(app):
    """
    Register views
    """

    # (`/` - main page)
    app.register_blueprint(base_view, url_prefix="/")

    # (`/categories`, `/vacancy_create`, `/<category_slug>`, `/vacancy/<vacancy_slug>`)
    app.register_blueprint(vacancies_view, url_prefix="/")

    # (`/signup`, `/login`, `/logout`, `/profile`)
    app.register_blueprint(auth_view, url_prefix="/")

    # (404, 408)
    app.register_blueprint(error_view)


def register_api_handlers(api):
    """
    Register api views
    """

    # Testing
    api.add_resource(TestConnection, "/ping")

    # Categories
    api.add_resource(CategoryAPI, "/categories")

    # Vacancies
    api.add_resource(VacancyAPI, "/vacancies/<category_slug>")

    # Auth
    api.add_resource(RegistrationUserAPI, "/auth/signup")
    api.add_resource(LoginUserAPI, "/auth/login")
