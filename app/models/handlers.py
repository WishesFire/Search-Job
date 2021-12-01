from app import db
from app.models.model import Category

CATEGORIES = {"Designer", "Accountant", "Lawyer", "Programmer",
              "Administrator", "Driver", "Cleaner", "Seller"}


def init_start_categories(app):
    with app.app_context():
        for index, category in enumerate(CATEGORIES):
            new_category = Category(id=index+1, name=category)
            db.session.add(new_category)
            db.session.commit()
