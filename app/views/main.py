"""
Views:
    - `home (/)`: Show main page with information about project
"""
import logging
from flask import Blueprint, render_template
from flask_login import current_user


base_view = Blueprint('base', __name__)


@base_view.route("/", methods=["GET"])
def home():
    """
    Show main home page
    :return: rendered template
    """
    logging.info(f"Enter to home page - {current_user.id}")
    return render_template("main_page.html", user=current_user)
