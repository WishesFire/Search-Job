from flask import Flask


def create_app():
    app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
    app.config.from_object("app.configs.config.TestBaseConfig")

    from .views.main import base_view

    app.register_blueprint(base_view, url_prefix="/")

    return app
