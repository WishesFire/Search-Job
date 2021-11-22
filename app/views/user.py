from flask import Blueprint


auth_view = Blueprint("auth", __name__)


@auth_view.route("/login")
def login():
    pass


@auth_view.route("/signup")
def signup():
    pass


@auth_view.route("/logout")
def logout():
    pass
