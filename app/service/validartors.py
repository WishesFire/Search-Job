"""
Service for validates incoming data
Validators:
    - `RegistrationFormValidator`: used to check_exists_email, check_password_similar
    - `LoginFormValidator`: used to check_user_exists
    - `VacancyFormValidator`: used to check_name, check_salary, check_category
"""
# pylint: disable=too-few-public-methods
# pylint: disable=no-else-return

from werkzeug.security import check_password_hash
from app.models.model import User, Category


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
    def __init__(self, password, user_checked):
        """
        :param password: user password
        :param user_checked: instance of the user from the database
        """
        self._password = password
        self._user_checked = user_checked

    def check_user_exists(self):
        """
        Checks the password cache and whether the user is in the database
        :return: Status, message about error or None
        """
        if not self._user_checked:
            msg = "User does not exist"
            return False, msg
        elif not check_password_hash(self._user_checked.password, self._password):
            msg = "Wrong password"
            return False, msg

        return True, None


class VacancyFormValidator:
    """
    Validator of vacancy input data
    """
    def __init__(self, name, salary, about, info, category=None):
        """
        :param name: vacancy name
        :param salary: vacancy salary
        :param about: information about job
        :param info: contact information
        """
        self.name = name
        self.salary = salary
        self.about = about
        self.info = info
        self.category = category

    def check_name(self):
        """
        :return: Title vacancy name
        """
        return self.name.title()

    def check_salary(self):
        """
        Checks on number salary
        :return: If not return False
        """
        if not isinstance(self.salary, float) or not isinstance(self.salary, int):
            return float(self.salary)
        return self.salary

    def check_category(self):
        """
        Checks if there is a category in the database
        :return: If category name find in database then return schema
        """
        if self.category:
            result = Category.query.filter_by(slug=str(self.category).title()).first()
            if result:
                return result
        return False
