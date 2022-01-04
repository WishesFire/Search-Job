"""
Configs for server
    - `TestBaseConfig`: server settings in test mode
    - `InitTestDataDB`: elements for testing
    - `ProductionBaseConfig`: server settings in production mode
"""

from dotenv import load_dotenv
from os import environ
import os


load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestBaseConfig(object):
    SECRET_KEY = environ.get("SECRET_KEY")
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    HOST = environ.get("HOST")
    PORT = environ.get("PORT")

    TESTING = True
    DEBUG = True
    LOGGING = False

    DB_USERNAME = environ.get("DB_USERNAME")
    DB_PASSWORD = environ.get("DB_PASSWORD")
    DB_NAME = environ.get("DB_NAME")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@localhost/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    ADMIN_MAIL = environ.get("ADMIN_MAIL")
    ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD")


class InitTestDataDB:
    CATEGORIES = {"Designer", "Accountant", "Lawyer", "Programmer",
                  "Administrator", "Driver", "Cleaner", "Seller"}
    USER_EMAIL = "aloha@gmail.com"
    USER_PASSWORD = "fskdop1241kfspdf"


class ProductionBaseConfig(TestBaseConfig):
    DEBUG = False
    TESTING = False
    LOGGING = True
