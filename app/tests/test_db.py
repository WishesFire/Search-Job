import pytest
from app import create_app
from app import db
from app.models.model import Category


@pytest.fixture
def created_db():
    """
    Create app context for db operations
    :return:
    """
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context() as created_db:
        yield created_db


def test_integrity_check(created_db):
    """
    Check element in category model
    :param created_db:
    :return:
    """
    res = Category.query.get(1)
    assert res.name == "Designer"
