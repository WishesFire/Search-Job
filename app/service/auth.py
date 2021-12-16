"""
Requires user registration and login utilities:
    - `util_signup`: validation data form and create new user in database
    - `util_login`: requirement validation parameters
"""

import logging
from werkzeug.security import generate_password_hash
from app.service.validartors import RegistrationFormValidator, LoginFormValidator
from app.models.model import User
from sqlalchemy import exc
from app import db


def util_signup(email, password_1, password_2):
    """
    Validation and create new user
    :param email: user mail
    :param password_1: first password
    :param password_2: second similar password
    :return: Status False or new_user
    """
    validator = RegistrationFormValidator(email, password_1, password_2)
    email_status, email_error_msg = validator.check_exists_email()
    password_status, password_error_msg = validator.check_password_similar()
    logging.info("Validation id DONE")

    if email_status and password_status:
        secure_password = generate_password_hash(password_1, method="sha256")
        try:
            new_user = User(email=email, password=secure_password)
            db.session.add(new_user)
            db.session.commit()
            logging.info("New user is created")
            return new_user
        except ValueError or exc.DataError:
            return False
    elif not email_status or not password_status:
        return False


def util_login(email, password):
    """
    Validation user
    :param email: user mail
    :param password: user password
    :return: validation user status, msg about error, user from bd
    """
    user = User.query.filter_by(email=email).first()
    validator = LoginFormValidator(email, password, user)
    user_status, user_error_msg = validator.check_user_exists()
    logging.info("Validation is DONE")

    return user_status, user_error_msg, user
