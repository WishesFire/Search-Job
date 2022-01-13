"""
This module works for restful api
VacancyAPI - (GET, POST, PUT, DELETE)
"""
# pylint: disable=unused-argument
# pylint: disable=literal-comparison

from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.model import Vacancy, Category
from app.rest.serializers import vacancies_schema
from app.service.validartors import VacancyFormValidator
from app import db
from .handlers import vacancy_post_args, vacancy_delete_args, vacancy_put_args, vacancy_get_args
from .utils import vacancy_check


class VacancyAPI(Resource):
    """
    Interaction with vacancies through restful api
    VacancyAPI - (GET, POST, PUT, DELETE)
    """

    @classmethod
    @vacancy_check
    def get(cls, category_slug):
        """
        Get all vacancies by category
        You can also get vacancies on the salary filter (parameter: filterSalary)
        :param category_slug: category slug
        :return: json
        """
        args = vacancy_get_args.parse_args()
        category = Category.query.filter_by(slug=category_slug).first()
        if args.get("filterSalary"):
            filter_salary = float(args.get("filterSalary"))
            all_vacancies = Vacancy.query.filter_by(category=category.id).filter(
                        Vacancy.salary <= filter_salary).all()
            if all_vacancies is []:
                return {"msg": "No vacancies were found for this filter"}, 200
        else:
            all_vacancies = Vacancy.query.filter_by(category=category.id).all()
        vacancies_serialize = vacancies_schema.dump(all_vacancies)
        return vacancies_serialize, 200

    @classmethod
    @vacancy_check
    @jwt_required()
    def post(cls, category_slug):
        """
        Create a new vacancy
        Parameters: name, salary, about, contacts
        :param category_slug: category slug
        :return: json
        """
        user_id = get_jwt_identity()

        args = vacancy_post_args.parse_args()
        name = args.get("name")
        salary = args.get("salary")
        about = args.get("about")
        contacts = args.get("contacts")

        validator = VacancyFormValidator(name, salary, about, contacts, category_slug)
        vacancy_name = validator.check_name()
        vacancy_salary = validator.check_salary()
        category = validator.check_category()

        if category:
            new_vacancy = Vacancy(name=vacancy_name, salary=vacancy_salary, info=about,
                                  contacts=contacts, user=user_id, category=category.id)
            db.session.add(new_vacancy)
            db.session.commit()

            return {"msg": "New vacancy successfully created", "id": new_vacancy.id}, 200

        return {"msg": "Category is not founded"}, 401

    @classmethod
    @vacancy_check
    @jwt_required()
    def put(cls, category_slug):
        """
        Update the opening vacancy
        Parameters: current_name, name, salary, about, contacts
        :return: json
        """
        user_id = get_jwt_identity()
        args = vacancy_put_args.parse_args()
        current_name = args.get("current_name")
        name = args.get("name")
        salary = args.get("salary")
        about = args.get("about")
        contacts = args.get("contacts")
        vacancy = Vacancy.query.filter_by(name=current_name, user=user_id).first()
        if vacancy:
            if name:
                vacancy.name = name
            elif salary:
                vacancy.salary = salary
            elif about:
                vacancy.info = about
            elif contacts:
                vacancy.contacts = contacts
            db.session.commit()

            return {"msg": "Vacancy successfully updated"}, 200

        return {"msg": "It's not your vacancy"}, 400

    @classmethod
    @vacancy_check
    @jwt_required()
    def delete(cls, category_slug):
        """
        Delete an existing vacancy
        Parameters: name
        :return: json
        """
        user_id = get_jwt_identity()
        args = vacancy_delete_args.parse_args()
        name = args.get("name")
        if Vacancy.query.filter_by(name=name, user=user_id).delete():
            db.session.commit()
            return {"msg": f"Vacancy - {name} successfully deleted"}, 200

        return {"msg": "Name of vacancy don't find"}, 400
