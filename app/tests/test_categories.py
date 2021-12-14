import pytest
from app import create_app, db
from app.models.model import Category


app = create_app()

CATEGORY_EXAMPLE = "Testing"


@pytest.fixture
def created_test_db():
    """
    Create app context for db operations
    """
    app.config["TESTING"] = True
    with app.app_context() as created_db:
        yield created_db


def check_category(flag):
    with app.app_context():
        check_exists = Category.query.filter_by(name=CATEGORY_EXAMPLE).first()

        if flag:
            if check_exists:
                Category.query.filter_by(name=CATEGORY_EXAMPLE).delete()

                new_category = Category(name=CATEGORY_EXAMPLE)
                db.session.add(new_category)
                db.session.commit()
        else:
            if not check_exists:
                new_category = Category(name=CATEGORY_EXAMPLE)
                db.session.add(new_category)
                db.session.commit()


def test_add_category(created_test_db):
    """
    Check add element category in database
    """

    with app.app_context():
        check_category(True)

        result = Category.query.filter_by(name=CATEGORY_EXAMPLE).first()
        assert result.name == "Testing"

        Category.query.filter_by(name=CATEGORY_EXAMPLE).delete()


def test_category_slug(created_test_db):
    """
    Check slug element category in database
    """

    with app.app_context():
        check_category(False)

        result = Category.query.filter_by(name=CATEGORY_EXAMPLE).first()
        assert result.slug

        Category.query.filter_by(name=CATEGORY_EXAMPLE).delete()
