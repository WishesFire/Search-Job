import pytest
from app import create_app
from app import db
from app.models.model import Category
from app.models.handlers import init_start_categories

app = create_app()


@pytest.fixture
def created_test_db():
    """
    Create app context for db operations
    """
    app.config["TESTING"] = True
    with app.app_context() as created_db:
        db.create_all()
        yield created_db


def test_integrity_category_check(created_test_db):
    """
    Check element in category model
    :param created_test_db: app context
    """
    with app.app_context():
        result = Category.query.get(1)
        if not result:
            init_start_categories()
            result = Category.query.get(1)
    assert result.name == "Designer"


def test_add_category(created_test_db):
    """
    Check add element category in database
    :param created_test_db: app context
    """
    category_example = "Testing"

    check_exists = Category.query.filter_by(name=category_example).first()
    if check_exists:
        Category.query.filter_by(name=category_example).delete()

    new_category = Category(name=category_example)
    db.session.add(new_category)
    db.session.commit()

    result = Category.query.filter_by(name=category_example).first()
    assert result.name == "Testing"
    db.session.rollback()


def test_get_vacancies_from_category(created_test_db):
    """
    Check vacancies with tied to category
    :param created_test_db: app context
    """
    pass

