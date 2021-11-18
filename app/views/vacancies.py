from flask import Blueprint, render_template


vacancies_view = Blueprint('vacancies', __name__)


@vacancies_view.route("/categories")
def categories():
    return render_template("categories.html")

