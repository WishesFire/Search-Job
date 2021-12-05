"""
Views:
    - `page_not_found (404)`: Show page with 404 error
    - `page_timeout (408)`: Show page with 408 error
"""

from flask import render_template, make_response, Blueprint

error_view = Blueprint("errors", __name__)


@error_view.app_errorhandler(404)
def page_not_found(error):
    """
    Create page with info about 404 error
    :param error: Instance error with information about problem
    :return: response with html template and status
    """
    return make_response(render_template("errors.html", status=error), 404)


@error_view.app_errorhandler(408)
def page_timeout(error):
    """
    Create page with info about 408 error
    :param error: Instance error with information about problem
    :return: response with html template and status
    """
    return make_response(render_template("errors.html", status=error), 408)
