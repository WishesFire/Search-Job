from .views.main import base_view
from .views.vacancies import vacancies_view
from .views.user import auth_view
from .views.error import error_view


def register_handlers(app):
    app.register_blueprint(base_view, url_prefix="/")
    app.register_blueprint(vacancies_view, url_prefix="/")
    app.register_blueprint(auth_view, url_prefix="/")
    app.register_blueprint(error_view)
