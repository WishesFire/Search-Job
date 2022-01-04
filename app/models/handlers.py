"""
This model defines is used to populate database with categories
    -`init_start_categories`: create new categories
"""

from app import db
from app.models.model import Category, User
from app.configs.config import InitTestDataDB, TestBaseConfig
from werkzeug.security import generate_password_hash


def init_start_categories(app):
    """
    Populate database with categories
    """
    with app.app_context():
        for index, category in enumerate(InitTestDataDB.CATEGORIES):
            new_category = Category(id=index+1, name=category)
            db.session.add(new_category)
        db.session.commit()


def init_test_user(app):
    """
    Populate database with test user
    """
    with app.app_context():
        secure_password = generate_password_hash(InitTestDataDB.USER_PASSWORD)
        new_user = User(email=InitTestDataDB.USER_EMAIL, password=secure_password)
        db.session.add(new_user)
        db.session.commit()


def init_admin_user(app):
    """
    Create admin user
    """
    with app.app_context():
        secure_password = generate_password_hash(TestBaseConfig.ADMIN_PASSWORD)
        admin = User(email=TestBaseConfig.ADMIN_MAIL, password=secure_password)
        db.session.add(admin)
        db.session.commit()
