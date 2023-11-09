"""
Views:
    - `about (/about)`: Show page with author information
"""
# pylint: disable=logging-fstring-interpolation

import logging
from flask import Blueprint, render_template
from flask_login import current_user


about_view = Blueprint('author', __name__)


@about_view.route("/about", methods=["GET"])
def about():
    """
    Show about page
    :return: rendered template
    """
    logging.info(f"Enter to about page - {current_user}")
    return render_template("about.html", user=current_user)
