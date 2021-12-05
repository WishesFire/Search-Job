"""
Views:
    - `sign_up (/signup)`: Register a new user in the system
    - `login (/login)`: Sign in to an existing account
    - `logout (/logout)`: Sing out from current account
    - `profile (/profile)`: User profile with functions:
        - Shows user vacancies
        - Create a new vacancy
"""

from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash
from app.service.validartors import RegistrationFormValidator, LoginFormValidator
from app.models.model import User
from flask_login import login_user, logout_user, login_required
from sqlalchemy import exc
from app import db


auth_view = Blueprint("auth", __name__)


@auth_view.route("/signup", methods=["GET", "POST"])
def sign_up():
    """
    Registration account
    :return: rendered template
    """
    if request.method == "POST":
        email = request.form.get("emailAddress")
        password_1 = request.form.get("password1")
        password_2 = request.form.get("password2")

        validator = RegistrationFormValidator(email, password_1, password_2)
        email_status, email_error_msg = validator.check_exists_email()
        password_status, password_error_msg = validator.check_password_similar()

        if email_status and password_status:
            secure_password = generate_password_hash(password_1, method="sha256")
            try:
                new_user = User(email=email, password=secure_password)
                db.session.add(new_user)
                db.session.commit()
            except ValueError or exc.DataError:
                flash("Error", category='error')
            else:
                login_user(new_user)

            return redirect(url_for("base.home"))
        elif not email_status:
            flash(f"Problem - {email_error_msg}", category='error')
        elif not password_status:
            flash(f"Problem - {password_error_msg}", category='error')

    return render_template("user/registration.html")


@auth_view.route("/login", methods=["GET", "POST"])
def login():
    """
    Log in account
    :return: rendered template
    """
    if request.method == "POST":
        email = request.form.get("emailAddress")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        validator = LoginFormValidator(email, password, user)
        user_status, user_error_msg = validator.check_user_exists()

        if user_status:
            login_user(user, remember=True)
            return redirect(url_for("auth.profile"))

        flash(f"Problem - {user_error_msg}", category='error')

    return render_template("user/login.html")


@auth_view.route("/logout")
@login_required
def logout():
    """
    Sing out
    :return: rendered template
    """
    logout_user()
    return redirect(url_for("base.home"))


@auth_view.route("/profile")
@login_required
def profile():
    """
    User profile
    :return: rendered template
    """
    return render_template("user/profile.html")
