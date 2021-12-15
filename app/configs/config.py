"""
Configs for server
"""

from dotenv import load_dotenv
from os import environ
import os


load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class TestBaseConfig(object):
    SECRET_KEY = environ.get("SECRET_KEY")
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


class InitTestDataDB:
    CATEGORIES = {"Designer", "Accountant", "Lawyer", "Programmer",
                  "Administrator", "Driver", "Cleaner", "Seller"}
    USER_EMAIL = "aloha@gmail.com"
    USER_PASSWORD = "fskdop1241kfspdf"


class ProductionBaseConfig(TestBaseConfig):
    DEBUG = False
    TESTING = False
    LOGGING = True
