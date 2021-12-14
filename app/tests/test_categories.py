import pytest
from app import db, create_app
from app.models.model import Category


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


def test_add_category(created_test_db):
    """
    Check add element category in database
    """
    category_example = "Testing"

    with app.app_context():
        check_exists = Category.query.filter_by(name=category_example).first()
        if check_exists:
            Category.query.filter_by(name=category_example).delete()

        new_category = Category(name=category_example)
        db.session.add(new_category)
        db.session.commit()

        result = Category.query.filter_by(name=category_example).first()
        assert result.name == "Testing"

        Category.query.filter_by(name=category_example).delete()


def test_category_slug(created_test_db):
    """
    Check slug element category in database
    """
    category_example = "Testing"

    with app.app_context():
        check_exists = Category.query.filter_by(name=category_example).first()
        if not check_exists:
            new_category = Category(name=category_example)
            db.session.add(new_category)
            db.session.commit()

        result = Category.query.filter_by(name=category_example).first()
        assert result.slug

        Category.query.filter_by(name=category_example).delete()
