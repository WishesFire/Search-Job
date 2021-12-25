"""
This module works for restful api
VacancyAPI - (GET, POST, DELETE)
"""

from flask_restful import Resource
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.model import Vacancy, Category
from sqlalchemy import exc
from app.rest.serializers import vacancies_schema
from .handlers import vacancy_post_args, vacancy_delete_args, vacancy_put_args
from app.service.validartors import VacancyFormValidator


class VacancyAPI(Resource):
    @classmethod
    def get(cls, category_slug):
        """
        Get all vacancies by category
        :param category_slug: category slug
        :return: json
        """
        try:
            category = Category.query.filter_by(slug=category_slug).first()
            if category:
                all_vacancies = Vacancy.query.filter_by(category=category.id).all()
                vacancies_serialize = vacancies_schema.dump(all_vacancies)
                return vacancies_serialize, 200
            return {"msg": f"Category with slug: {category} don't exist"}, 401

        except exc.ArgumentError:
            return {"msg": "Invalid or conflicting function argument is supplied"}
        except exc.SQLAlchemyError:
            return {"msg": "Execution of a database operation fails"}
        except Exception as error:
            return {"msg": error}

    @classmethod
    @jwt_required()
    def post(cls, category_slug):
        """
        Create a new vacancy
        :param category_slug: category slug
        :return: json
        """
        try:
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

        except exc.ArgumentError:
            return {"msg": "Invalid or conflicting function argument is supplied"}
        except exc.SQLAlchemyError:
            return {"msg": "Execution of a database operation fails"}
        except Exception as error:
            return {"msg": error}

    @classmethod
    @jwt_required()
    def put(cls, category_slug):
        """
        Update the opening vacancy
        :param category_slug: category slug
        :return: json
        """
        try:
            user_id = get_jwt_identity()
            args = vacancy_put_args.parse_args()
            current_name = args.get("current_name")
            name = args.get("name")
            salary = args.get("salary")
            about = args.get("about")
            contacts = args.get("contacts")
            vacancy = Vacancy.query.filter_by(name=current_name, user=user_id).first()
            if name:
                vacancy.name = name
            elif salary:
                vacancy.salary = salary
            elif about:
                vacancy.info = about
            elif contacts:
                vacancy.contacts = contacts
            db.session.commit()

            return {"msg": "Vacancy successfully updated"}

        except exc.ArgumentError:
            return {"msg": "Invalid or conflicting function argument is supplied"}
        except exc.SQLAlchemyError:
            return {"msg": "Execution of a database operation fails"}
        except Exception as error:
            return {"msg": error}

    @classmethod
    @jwt_required()
    def delete(cls, category_slug):
        """
        Delete an existing vacancy
        :param category_slug: category slug
        :return: json
        """
        try:
            user_id = get_jwt_identity()
            args = vacancy_delete_args.parse_args()
            name = args.get("name")
            Vacancy.query.filter_by(name=name, user=user_id).delete()
            db.session.commit()

            return {"msg": f"Vacancy - {name} successfully deleted"}

        except exc.ArgumentError:
            return {"msg": "Invalid or conflicting function argument is supplied"}
        except exc.SQLAlchemyError:
            return {"msg": "Execution of a database operation fails"}
        except Exception as error:
            return {"msg": error}
