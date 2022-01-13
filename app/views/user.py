"""
Views:
    - `sign_up (/signup)`: Register a new user in the system
    - `login (/login)`: Sign in to an existing account
    - `logout (/logout)`: Sing out from current account
    - `profile (/profile)`: User profile with functions:
        - Shows user vacancies
        - Create a new vacancy
"""
# pylint: disable=ungrouped-imports
# pylint: disable=logging-fstring-interpolation

import json
import logging
from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask_admin.contrib.sqla import ModelView
from app.service.auth import util_signup, util_login
from app.models.model import User, Vacancy
from app import db
from app.configs.config import TestBaseConfig


auth_view = Blueprint("auth", __name__)


@auth_view.route("/signup", methods=["GET", "POST"])
def sign_up():
    """
    Registration account
    :return: rendered template
    """
    if request.method == "POST":
        logging.info("User POST data through registration form")
        email = request.form.get("emailAddress")
        password_1 = request.form.get("password1")
        password_2 = request.form.get("password2")
        user = util_signup(email, password_1, password_2)
        if user:
            login_user(user)

            return redirect(url_for("base.home"))
        flash("Problem with registration", category='error')

    return render_template("user/registration.html")


@auth_view.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in account
    :return: rendered template
    """
    if request.method == "POST":
        logging.info("User POST data through login form")
        email = request.form.get("emailAddress")
        password = request.form.get("password")

        user_status, user_error_msg, user = util_login(email, password)

        if user_status:
            logging.info("Login user")
            login_user(user, remember=True)
            return redirect(url_for("auth.profile"))

        flash(f"Problem - {user_error_msg}", category='error')

    return render_template("user/login.html")


@auth_view.route("/logout", methods=["GET"])
@login_required
def logout():
    """
    Sing out
    :return: rendered template
    """
    logging.info("Logout user")
    logout_user()
    return redirect(url_for("base.home"))


@auth_view.route("/profile", methods=["GET", "DELETE"])
@login_required
def profile():
    """
    Profile of the user with his vacancies and the ability to create new ones
    Can delete own vacancies
    :return: rendered template
    """
    if request.method == "DELETE":
        data = json.loads(request.data)
        logging.info(f"Deleted data - {data['name']}")
        if data["name"]:
            Vacancy.query.filter_by(name=data["name"], user=current_user.id).delete()
            db.session.commit()
        return "Deleted"

    logging.info("User open profile")
    user = User.query.filter_by(email=current_user.email).first()
    content = {"user": current_user, "exists_vacancies": user.vacancies}
    return render_template("user/profile.html", **content)


class JobAdminModelView(ModelView):
    """
    User admin check
    """
    def is_accessible(self):
        """
        Check whether the user is registered and logged in as an administrator
        """
        if not current_user.is_authenticated or current_user.email != TestBaseConfig.ADMIN_MAIL:
            return False
        return True

    def inaccessible_callback(self, name, **kwargs):
        """
        Redirects to the registration page
        """
        return redirect(url_for('auth.login'))
