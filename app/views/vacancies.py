from flask import Blueprint, render_template
from app.models.model import Category


vacancies_view = Blueprint('vacancies', __name__)


@vacancies_view.route("/categories", methods=["GET"])
def categories_show():
    categories = Category.query.all()
    return render_template("categories.html", categories=categories)


@vacancies_view.route("/<category_slug>", methods=["GET"])
def vacancies_show(category_slug):
    return render_template("vacancies.html")

