"""
Service for validates incoming data
Validators:
    - `RegistrationFormValidator`: used to check_exists_email and check_password_similar
    - `LoginFormValidator`: used to check_user_exists
"""

from app.models.model import User
from werkzeug.security import check_password_hash


class RegistrationFormValidator:
    """
    Validator of registration input data
    """
    def __init__(self, email, password1, password2):
        """
        :param email: user mail
        :param password1: first user password
        :param password2: second user password
        """
        self.email = email
        self.password1 = password1
        self.password2 = password2

    def check_exists_email(self):
        """
        Checks for such mail in the database
        :return: Status, message about error or None
        """
        if User.query.filter_by(email=self.email).first():
            msg = "Email already exists"
            return False, msg
        return True, None

    def check_password_similar(self):
        """
        Checks if the first and second passwords match
        :return: Status, message about error or None
        """
        if self.password1 != self.password2:
            msg = "Passwords do not match"
            return False, msg
        return True, None


class LoginFormValidator:
    """
    Validator of login input data
    """
    def __init__(self, email, password, user_checked):
        """
        :param email: user mail
        :param password: user password
        :param user_checked: instance of the user from the database
        """
        self.email = email
        self.password = password
        self.user_checked = user_checked

    def check_user_exists(self):
        """
        Checks the password cache and whether the user is in the database
        :return: Status, message about error or None
        """
        if not self.user_checked:
            msg = "User does not exist"
            return False, msg
        elif not check_password_hash(self.user_checked.password, self.password):
            msg = "Wrong password"
            return False, msg

        return True, None
