import pytest
from app import create_app, db

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


def test_create_vacancy(client):
    """
    Check create new vacancy using a user profile
    /vacancy_create - create new vacancy
    :param client: cope app client
    :return: Passed status if code is similar
    """
    example_name = "Hunter"
    example_salary = 3000
    example_about = "Interesting job"
    example_contacts = "example@mail.com"
    example_category = "Designer"

    result = client.post("/vacancy_create", data={"name": example_name, "salary": example_salary,
                                                  "about": example_about, "contacts": example_contacts,
                                                  "category": example_category}, follow_redirects=True)
    assert result.status_code == STATUS_CODE


def test_vacancy_detail(client):
    """
    Check vacancy detail
    /vacancy/<vacancy_slug> - information about vacancy
    :param client: cope app client
    :return: Passed status if code is similar
    """
    result = client.get("/vacancy/movies", follow_redirects=True)
    assert result.status_code == STATUS_CODE
    assert result.data


def test_vacancy_filter(client):
    """
    Check vacancy filter by salary
    /vacancy/<vacancy_slug> - information about vacancy
    :param client: cope app client
    :return: Passed status if code is similar
    """
    result = client.post("/designer", data={"salary-avg": 500})
    assert result.status_code == STATUS_CODE
