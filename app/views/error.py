from flask import render_template, make_response, Blueprint

error_view = Blueprint("errors", __name__)


@error_view.app_errorhandler(404)
def page_not_found(error):
    return make_response(render_template("errors.html", status=error), 404)


@error_view.app_errorhandler(408)
def page_timeout(error):
    return make_response(render_template("errors.html", status=error), 408)
