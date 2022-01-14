"""
Testing is related to the interaction with categories functions
"""
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import

from app import db
from app.models.model import Category
from app.service.category_service import CategoryService
from . import client, app

STATUS_CODE = 200


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


def test_add_category():
    """
    Check add element category in database
    """
    category_example = "Testing"

    with app.app_context():
        check_exists = CategoryService.find_category_by_name(category_example)
        if check_exists:
            Category.query.filter_by(name=category_example).delete()

        new_category = Category(name=category_example)
        db.session.add(new_category)
        db.session.commit()

        result = CategoryService.find_category_by_name(category_example)
        assert result.name == "Testing"

        Category.query.filter_by(name=category_example).delete()


def test_category_slug():
    """
    Check slug element category in database
    """
    category_example = "Testing"

    with app.app_context():
        check_exists = CategoryService.find_category_by_name(category_example)
        if not check_exists:
            new_category = Category(name=category_example)
            db.session.add(new_category)
            db.session.commit()

        result = CategoryService.find_category_by_name(category_example)
        assert result.slug

        Category.query.filter_by(name=category_example).delete()
