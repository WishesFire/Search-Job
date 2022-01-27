"""
Views:
    - `categories_show (/categories)`: Show all jobs categories
    - `vacancies_show (/<category_slug>)`: Show all vacancies for specific category
    - `vacancy_create (/vacancy_create)`: Show vacancy create form
    - `vacancy_detail (/vacancy/<vacancy_slug>)`: Show detail about vacancy
"""
# pylint: disable=logging-fstring-interpolation
# pylint: disable=wrong-import-order
# pylint: disable=ungrouped-imports
# pylint: disable=simplifiable-if-statement

import logging
import json
from flask import Blueprint, render_template, request, redirect, url_for
from flask_mail import Message
from flask_login import current_user, login_required
from app.configs.config import TestBaseConfig
from app.service.validartors import VacancyFormValidator
from app.service.category_service import CategoryService
from app.service.vacancy_service import VacancyService
from app.service.user_service import UserService
from app import mail


vacancies_view = Blueprint('vacancies', __name__)


@vacancies_view.route("/categories", methods=["GET"])
def categories_show():
    """
    Show categories
    :return: rendered template
    """
    logging.info("Show all categories")
    categories = CategoryService.get_all_categories()
    average_salary = {}
    all_count_vacancies = 0
    for category in categories:
        average = 0
        for vacancy in category.vacancies:
            average += vacancy.salary
        if average > 0:
            average_salary[category.name] = int(average / len(category.vacancies))
        else:
            average_salary[category.name] = 0
        all_count_vacancies += len(category.vacancies)
    content = {"categories": categories, "count_vacancies": all_count_vacancies,
               "average_salary": average_salary, "user": current_user}
    logging.info(f"All categories - {categories}")
    return render_template("categories.html", **content)


@vacancies_view.route("/vacancy_create", methods=["GET", "POST"])
@login_required
def vacancy_create():
    """
    Vacancy information form (Name, salary, about, notification, contacts).
    Then the vacancy appears in the list
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
        validator = VacancyFormValidator(vacancy_name, vacancy_salary,
                                         vacancy_about, vacancy_contacts)
        vacancy_name = validator.check_name()
        vacancy_salary = validator.check_salary()
        logging.info("Validation is DONE")

        category = CategoryService.find_category_by_name(vacancy_category)
        VacancyService.create_new_vacancy(vacancy_name, vacancy_salary,
                                          vacancy_about, vacancy_contacts,
                                          vacancy_notification, current_user.id, category.id)
        logging.info("New vacancy created")

        return redirect(url_for("auth.profile"))

    categories = CategoryService.get_all_categories()
    content = {"categories": categories, "user": current_user}
    return render_template("vacancy_create.html", **content)


@vacancies_view.route("/<category_slug>/vacancies", methods=["GET", "POST"])
def vacancies_show(category_slug):
    """
    Show vacancies specific category
    Filters salary vacancies
    :param category_slug: used for url
    :return: rendered template
    """
    page_count = request.args.get("page", 1, type=int)
    if request.method == "POST":
        salary_average = request.form.get("salary-avg")
        if salary_average:
            logging.info(f"Salary filter get - {salary_average}")
            salary_average = float(salary_average)
            category = CategoryService.find_category_by_slug(category_slug)
            vacancies = VacancyService.find_vacancies_by_filter(
                                          category.id, salary_average,
                                          (page_count, TestBaseConfig.PAGINATION_PAGE))
            logging.info(f"Current category - {category.name}")
            logging.info(f"All filtered vacancies - {vacancies}")
            content = {"category_vacancies": vacancies, "category_slug": category_slug,
                       "user": current_user, "filter_flag": True}
            return render_template("vacancies.html", **content)

    category = CategoryService.find_category_by_slug(category_slug)
    if category:
        vacancies = VacancyService.find_vacancies_by_category(category.id,
                                                              (page_count,
                                                               TestBaseConfig.PAGINATION_PAGE))
        content = {"category_vacancies": vacancies, "category_slug": category_slug,
                   "user": current_user, "filter_flag": False}
        return render_template("vacancies.html", **content)
    return redirect(url_for("base.home"))


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
            current_vacancy = VacancyService.find_vacancy_by_slug(vacancy_slug)
            owner = UserService.find_user_by_id(current_vacancy.user)
            if current_user.id != owner.id:
                msg = Message("Someone watch your contacts", sender=TestBaseConfig.MAIL_USERNAME,
                              recipients=[owner.email])
                msg.body = f"Someone found out about your job " \
                           f"in this vacancy - {current_vacancy.name}"
                mail.send(msg)
                return "Message sent"
            return "Message don't send"

    current_vacancy = VacancyService.find_vacancy_by_slug(vacancy_slug)
    logging.info(f"Show vacancy detail - {current_vacancy.name}")
    content = {"vacancy": current_vacancy, "user": current_user}
    return render_template("vacancy.html", **content)
