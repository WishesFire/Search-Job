"""
Views:
    - `categories_show (/categories)`: Show all jobs categories
    - `vacancies_show` (/<category_slug>)`: Show all vacancies for specific category
"""

from flask import Blueprint, render_template
from flask_login import current_user
from app.models.model import Category


vacancies_view = Blueprint('vacancies', __name__)


@vacancies_view.route("/categories", methods=["GET"])
def categories_show():
    """
    Show categories
    :return: rendered template
    """
    categories = Category.query.all()
    content = {"categories": categories, "user": current_user}
    return render_template("categories.html", **content)


@vacancies_view.route("/<category_slug>", methods=["GET"])
def vacancies_show(category_slug):
    """
    Show vacancies
    :param category_slug: used for url
    :return: rendered template
    """
    return render_template("vacancies.html", user=current_user)

