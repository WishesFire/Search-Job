"""
This module has all the necessary functions to interact with the User model
"""

from app.models.model import User
from app import db


class UserService:
    """
    CRUD operations on User model
    """

    @staticmethod
    def find_user_by_id(current_vacancy_user: int) -> User:
        """
        Takes user by user id
        :param current_vacancy_user:
        :return: user object
        """
        return User.query.filter_by(id=current_vacancy_user).first()

    @staticmethod
    def find_user_by_email(email: str) -> User:
        """
        Takes user by user email
        :param email: user mail
        :return: user object
        """
        return User.query.filter_by(email=email).first()

    @staticmethod
    def create_new_user(email: str, password: str) -> User:
        """
        Create new user
        :param email: user mail
        :param password: user password
        :return: user object
        """
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def delete_user(email: str) -> None:
        """
        Delete user
        :param email: user mail
        :return: user object
        """
        User.query.filter_by(email=email).delete()
        db.session.commit()
