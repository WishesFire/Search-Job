"""
Views:
    - `categories_show (/categories)`: Show all jobs categories
    - `vacancies_show (/<category_slug>)`: Show all vacancies for specific category
    - `vacancy_create (/vacancy_create)`: Show vacancy create form
    - `vacancy_detail (/vacancy/<vacancy_slug>)`: Show detail about vacancy
"""

from flask import Blueprint, render_template, request, redirect, url_for
from app.service.validartors import VacancyFormValidator
from flask_login import current_user
from app.models.model import Category, Vacancy
from app import db


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


@vacancies_view.route("/vacancy_create", methods=["GET", "POST"])
def vacancy_create():
    """
    Vacancy information form
    :return: rendered template
    """
    if request.method == "POST":
        vacancy_name = request.form.get("name")
        vacancy_salary = request.form.get("salary")
        vacancy_about = request.form.get("about")
        vacancy_contacts = request.form.get("contacts")
        vacancy_category = request.form.get("category")

        validator = VacancyFormValidator(vacancy_name, vacancy_salary, vacancy_about, vacancy_contacts)
        vacancy_name = validator.check_name()
        vacancy_salary = validator.check_salary()

        category = Category.query.filter_by(name=vacancy_category).first()

        new_vacancy = Vacancy(name=vacancy_name, salary=vacancy_salary, info=vacancy_about,
                              contacts=vacancy_contacts, user=current_user.id, category=category.id)
        db.session.add(new_vacancy)
        db.session.commit()

        return redirect(url_for("auth.profile"))

    categories = Category.query.all()
    content = {"categories": categories, "user": current_user}
    return render_template("vacancy_create.html", **content)


@vacancies_view.route("/<category_slug>", methods=["GET"])
def vacancies_show(category_slug):
    """
    Show vacancies
    :param category_slug: used for url
    :return: rendered template
    """
    category = Category.query.filter_by(slug=category_slug).first()
    content = {"category_vacancies": category, "user": current_user}
    return render_template("vacancies.html", **content)


@vacancies_view.route("/vacancy/<vacancy_slug>", methods=["GET"])
def vacancy_detail(vacancy_slug):
    """
    Show detail about specific vacancy
    :param vacancy_slug:
    :return: rendered template
    """
    current_vacancy = Vacancy.query.filter_by(slug=vacancy_slug).first()
    content = {"vacancy": current_vacancy, "user": current_user}
    return render_template("vacancy.html", **content)
