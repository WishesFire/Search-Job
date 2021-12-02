import pytest
from app import create_app

STATUS_CODE = 200


@pytest.fixture
def client():
    """
    Create new application as client
    :return: copy app client
    """
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def created_app():
    """
    Create new application for checking configs
    :return: app
    """
    app = create_app()
    app.config.from_object("app.configs.config.TestBaseConfig")
    return app


def test_config(created_app):
    """
    Check application config
    :param created_app:
    :return:
    """
    assert created_app.config["DEBUG"]
    assert created_app.config["SECRET_KEY"]
    assert created_app.config["DB_USERNAME"]
    assert created_app.config["DB_PASSWORD"]
    assert created_app.config["DB_NAME"]


def test_status_main(client):
    """
    / - main_page
    :param client: copy app client
    :return: Passed status if code is similar
    """
    res = client.get("/")
    assert STATUS_CODE == res.status_code


def test_status_categories(client):
    """
    /categories - categories
    :param client: copy app client
    :return: Passed status if code is similar
    """
    res = client.get("/categories")
    assert STATUS_CODE == res.status_code
