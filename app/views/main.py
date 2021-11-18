from flask import Blueprint, render_template


base_view = Blueprint('base', __name__)


@base_view.route("/")
def home():
    return render_template("main_page.html")
