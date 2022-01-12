"""
Views:
    - `categories_show (/categories)`: Show all jobs categories
    - `vacancies_show (/<category_slug>)`: Show all vacancies for specific category
    - `vacancy_create (/vacancy_create)`: Show vacancy create form
    - `vacancy_detail (/vacancy/<vacancy_slug>)`: Show detail about vacancy
"""

import logging
import json
from flask import Blueprint, render_template, request, redirect, url_for
from flask_mail import Message
from app.configs.config import TestBaseConfig
from app.service.validartors import VacancyFormValidator
from flask_login import current_user, login_required
from app.models.model import Category, Vacancy, User
from app import db, mail


vacancies_view = Blueprint('vacancies', __name__)


@vacancies_view.route("/categories", methods=["GET"])
def categories_show():
    """
    Show categories
    :return: rendered template
    """
    logging.info("Show all categories")
    categories = Category.query.all()
    average_salary = {}
    for category in categories:
        average = 0
        for vacancy in category.vacancies:
            average += vacancy.salary
        if average > 0:
            average_salary[category.name] = int(average / len(category.vacancies))
        else:
            average_salary[category.name] = 0
    content = {"categories": categories, "average_salary": average_salary, "user": current_user}
    logging.info(f"All categories - {categories}")
    return render_template("categories.html", **content)


@vacancies_view.route("/vacancy_create", methods=["GET", "POST"])
@login_required
def vacancy_create():
    """
    Vacancy information form (Name, salary, about, notification, contacts). Then the vacancy appears in the list
    :return: rendered template
    """
    if request.method == "POST":
        logging.info("User POST vacancy_create")
        vacancy_name = request.form.get("name")
        vacancy_salary = request.form.get("salary")
        vacancy_about = request.form.get("about")
        vacancy_contacts = request.form.get("contacts")
        vacancy_category = request.form.get("category")
        if request.form.get("notify"):
            vacancy_notification = True
        else:
            vacancy_notification = False
        logging.info("Get vacancy data from vacancy creating form")

        validator = VacancyFormValidator(vacancy_name, vacancy_salary, vacancy_about, vacancy_contacts)
        vacancy_name = validator.check_name()
        vacancy_salary = validator.check_salary()
        logging.info("Validation is DONE")

        category = Category.query.filter_by(name=vacancy_category).first()
        new_vacancy = Vacancy(name=vacancy_name, salary=vacancy_salary, info=vacancy_about,
                              contacts=vacancy_contacts, notification=vacancy_notification,
                              user=current_user.id, category=category.id)
        db.session.add(new_vacancy)
        db.session.commit()
        logging.info("New vacancy created")

        return redirect(url_for("auth.profile"))

    categories = Category.query.all()
    content = {"categories": categories, "user": current_user}
    return render_template("vacancy_create.html", **content)


@vacancies_view.route("/<category_slug>", methods=["GET", "POST"])
def vacancies_show(category_slug):
    """
    Show vacancies specific category
    Filters salary vacancies
    :param category_slug: used for url
    :return: rendered template
    """
    if request.method == "POST":
        salary_average = request.form.get("salary-avg")
        if salary_average:
            logging.info(f"Salary filter get - {salary_average}")
            salary_average = float(salary_average)
            category = Category.query.filter_by(slug=category_slug).first()
            logging.info(f"Current category - {category.name}")
            vacancies = Vacancy.query.filter_by(category=category.id).filter(Vacancy.salary <= salary_average).all()
            logging.info(f"All filtered vacancies - {vacancies}")
            content = {"category_vacancies": vacancies, "user": current_user, "filter_flag": True}
            return render_template("vacancies.html", **content)

    category = Category.query.filter_by(slug=category_slug).first()
    content = {"category_vacancies": category, "user": current_user, "filter_flag": False}
    return render_template("vacancies.html", **content)


@vacancies_view.route("/vacancy/<vacancy_slug>", methods=["GET", "POST"])
@login_required
def vacancy_detail(vacancy_slug):
    """
    Show detail about specific vacancy (title, salary, information about vacancy, contacts)
    :param vacancy_slug:
    :return: rendered template
    """
    if request.method == "POST":
        data = json.loads(request.data)
        if data["notification"]:
            current_vacancy = Vacancy.query.filter_by(slug=vacancy_slug).first()
            owner = User.query.filter_by(id=current_vacancy.user).first()
            msg = Message("Someone watch your contacts", sender=TestBaseConfig.MAIL_USERNAME,
                          recipients=[owner.email])
            msg.body = f"Someone found out about your job in this vacancy - {current_vacancy.name}"
            mail.send(msg)
            return "Message sent"

    current_vacancy = Vacancy.query.filter_by(slug=vacancy_slug).first()
    logging.info(f"Show vacancy detail - {current_vacancy.name}")
    content = {"vacancy": current_vacancy, "user": current_user}
    return render_template("vacancy.html", **content)
