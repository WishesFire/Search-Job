import pytest
from app import create_app, db
from app.models.model import Category


app = create_app()

STATUS_CODE = 200


@pytest.fixture
def client():
    """
    Create new application as client
    :return: copy app client
    """
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


def test_status_categories(client):
    """
    Check get categories page
    /categories - categories
    :param client: copy app client
    :return: Passed status if code is similar
    """
    res = client.get("/categories")
    assert STATUS_CODE == res.status_code


def test_status_specific_category(client):
    """
    Check get vacancies page
    /<category_slug> - specific category
    :param client: cope app client
    :return: Passed status if code is similar
    """
    res = client.get("/designer")
    assert STATUS_CODE == res.status_code


def test_add_category(client):
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


def test_category_slug(client):
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
