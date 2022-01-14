"""
This module has all the necessary functions to interact with the Vacancy model
"""

from app.models.model import Vacancy
from app import db


class VacancyService:
    """
    CRUD operations on Vacancy model
    """

    @staticmethod
    def create_new_vacancy(vacancy_name: str, vacancy_salary: float,
                           vacancy_about: str, vacancy_contacts: str,
                           vacancy_notification: bool, current_user_id: int,
                           category_id: int) -> int:
        """
        Creates a new vacancy and writes to the database
        :param vacancy_name: vacancy name
        :param vacancy_salary: salary of this vacancy
        :param vacancy_about: information about vacancy
        :param vacancy_contacts: contacts
        :param vacancy_notification: notification for email
        :param current_user_id: id user for check exist vacancy
        :param category_id: vacancy category
        :return: vacancy id
        """
        new_vacancy = Vacancy(name=vacancy_name, salary=vacancy_salary, info=vacancy_about,
                              contacts=vacancy_contacts, notification=vacancy_notification,
                              user=current_user_id, category=category_id)
        db.session.add(new_vacancy)
        db.session.commit()

        return new_vacancy.id

    @staticmethod
    def find_vacancies_by_filter(category_id: int, salary_average: float) -> Vacancy:
        """
        Takes vacancies on the price filter
        :param category_id:
        :param salary_average:
        :return: vacancy object
        """
        return Vacancy.query.filter_by(category=category_id).\
            filter(Vacancy.salary <= salary_average).all()

    @staticmethod
    def find_vacancy_by_slug(vacancy_slug: str) -> Vacancy:
        """
        Takes vacancies by vacancy slug
        :param vacancy_slug:
        :return: vacancy object
        """
        return Vacancy.query.filter_by(slug=vacancy_slug).first()

    @staticmethod
    def find_vacancy_by_name_user(name: str, user: int) -> Vacancy:
        """
        Takes vacancies by vacancy slug
        :param name: vacancy name
        :param user: user id
        :return: vacancy object
        """
        return Vacancy.query.filter_by(name=name, user=user).first()

    @staticmethod
    def delete_vacancy_by_name_user(name: str, user: int) -> None:
        """
        Delete vacancy with parameters: name, user
        :param name: vacancy name
        :param user: user id
        """
        Vacancy.query.filter_by(name=name, user=user).delete()
        db.session.commit()

    @staticmethod
    def find_vacancies_by_category(category: int) -> Vacancy:
        """
        Takes vacancies by category
        :param category: category name
        :return: vacancy object
        """
        return Vacancy.query.filter_by(category=category).all()

    @staticmethod
    def find_vacancies_current_user(user: int) -> Vacancy:
        """
        Takes vacancies only user who created them
        :param user: user id
        :return: vacancy object
        """
        return Vacancy.query.filter_by(user=user).all()
