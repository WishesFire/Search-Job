import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_status_main(client):
    res = client.get("/")
    assert 200 == res.status_code


def test_status_categories(client):
    res = client.get("/categories")
    assert 200 == res.status_code
