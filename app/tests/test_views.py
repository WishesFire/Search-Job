import pytest
from app import create_app


STATUS_CODE = 200


@pytest.fixture
def client():
    """
    Create new application
    :return: copy app client
    """
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


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
