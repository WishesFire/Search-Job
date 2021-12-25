"""
Views:
    - `sign_up (/signup)`: Register a new user in the system
    - `login (/login)`: Sign in to an existing account
    - `logout (/logout)`: Sing out from current account
    - `profile (/profile)`: User profile with functions:
        - Shows user vacancies
        - Create a new vacancy
"""

import json
import logging
from flask import Blueprint, request, redirect, url_for, render_template, flash
from app.service.auth import util_signup, util_login
from app.models.model import User, Vacancy
from flask_login import login_user, logout_user, login_required, current_user


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
        else:
            flash(f"Problem with registration", category='error')

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
    :return: rendered template
    """
    if request.method == "DELETE":
        data = json.loads(request.data)
        logging.info(f"Deleted data - {data['name']}")
        if data["name"]:
            Vacancy.query.filter_by(name=data["name"], user=current_user.id).delete()

    logging.info("User open profile")
    user = User.query.filter_by(email=current_user.email).first()
    content = {"user": current_user, "exists_vacancies": user.vacancies}
    return render_template("user/profile.html", **content)
