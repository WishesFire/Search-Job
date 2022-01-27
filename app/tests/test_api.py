"""
Testing is related to the interaction with restful api
"""

# pylint: disable=redefined-outer-name
# pylint: disable=unused-import
# pylint: disable=global-statement

import json
from app.service.user_service import UserService
from . import client, app


LOGIN_TOKEN = ""
CATEGORY_SLUG = "designer"
NAME = "123123"
SALARY = 233.0
ABOUT = "Good job"
CONTACTS = "+390423423"
FILTER_SALARY = 100.0

EMAIL = "lol@mail.com"
PASSWORD1 = "12345"
PASSWORD2 = "12345"


def test_connection(client):
    """
    test `/api/ping` - Check connection
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.get("/api/ping")
    assert response.status_code == 200
    assert response.json["Ping"] == "Pong"


def test_get_categories(client):
    """
    test `/api/categories` - Get all categories
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.get("/api/categories")
    assert response.status_code == 200
    assert response.json


def test_signup_login(client):
    """
    test `/api/auth/signup` - Create new user
    test `/api/auth/login` - Login in user and get token
    :param client: cope app client
    :return: Passed status if code is similar
    """
    global LOGIN_TOKEN

    with app.app_context():
        UserService.delete_user(EMAIL)

    response = client.post("/api/auth/signup",
                           headers={"Content-Type": "application/json"},
                           data=json.dumps(
                               {"email": EMAIL, "password1": PASSWORD1,
                                "password2": PASSWORD2}))

    assert response.status_code == 200
    assert response.json["msg"] == "User successfully created"

    response = client.post("/api/auth/login", headers={"Content-Type": "application/json"},
                           data=json.dumps({"email": EMAIL, "password": PASSWORD1}))
    LOGIN_TOKEN = response.json['token']

    assert response.status_code == 200
    assert response.json["token"] == LOGIN_TOKEN


def test_api_profile(client):
    """
    test `/api/auth/profile` - Show only user vacancies
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.get("/api/auth/profile",
                          headers={"Content-Type": "application/json",
                                   "Authorization": f"Bearer {LOGIN_TOKEN}"})
    assert response.status_code == 200


def test_get_vacancies(client):
    """
    test `/api/vacancies/category_slug` (GET) - Get vacancies at slug
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.get(f"/api/vacancies/{CATEGORY_SLUG}")
    assert response.status_code == 200


def test_get_pagination_vacancies(client):
    """
    test `/api/vacancies/category_slug` (GET) - Get vacancies at slug, checking
    number of vacancies in json.
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.get(f"/api/vacancies/{CATEGORY_SLUG}")
    assert len(response.json["data"]) < 6


def test_post_vacancy(client):
    """
    test `api/vacancies/category_slug` (POST) - Create new test vacancy
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.post(f"/api/vacancies/{CATEGORY_SLUG}",
                           headers={"Content-Type": "application/json",
                                    "Authorization": f"Bearer {LOGIN_TOKEN}"},
                           data=json.dumps({"name": NAME, "salary": SALARY,
                                            "about": ABOUT, "contacts": CONTACTS}))
    assert response.status_code == 200
    assert response.json["msg"] == "New vacancy successfully created"


def test_put_vacancy(client):
    """
    test `api/vacancies/category_slug` (PUT) - Update test vacancy
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.put(f"/api/vacancies/{CATEGORY_SLUG}",
                          headers={"Content-Type": "application/json",
                                   "Authorization": f"Bearer {LOGIN_TOKEN}"},
                          data=json.dumps({"current_name": NAME, "salary": 99999}))
    assert response.status_code == 200
    assert response.json["msg"] == "Vacancy successfully updated"


def test_delete_vacancy(client):
    """
    test `api/vacancies/category_slug` (DELETE) - Delete test vacancy
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.delete(f"/api/vacancies/{CATEGORY_SLUG}",
                             headers={"Content-Type": "application/json",
                                      "Authorization": f"Bearer {LOGIN_TOKEN}"},
                             data=json.dumps({"name": NAME}))
    assert response.status_code == 200
    assert response.json["msg"] == f"Vacancy - {NAME} successfully deleted"


def test_get_vacancies_filter(client):
    """
    test `/api/vacancies/category_slug` - Get vacancies at slug with filterSalary
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.get(f"/api/vacancies/{CATEGORY_SLUG}",
                          data=json.dumps({"filterSalary": FILTER_SALARY}))
    assert response.status_code == 200


def test_post_vacancy_error_not_data(client):
    """
    test `api/vacancies/category_slug` (POST) - Create error vacancy with bad category slug
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.get("/api/vacancies/111")
    assert response.status_code == 404


def test_put_vacancy_error(client):
    """
    test `api/vacancies/category_slug` (PUT) - Create update error vacancy with not vacancy your
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.put(f"/api/vacancies/{CATEGORY_SLUG}",
                          headers={"Content-Type": "application/json",
                                   "Authorization": f"Bearer {LOGIN_TOKEN}"},
                          data=json.dumps({"current_name": 99999999}))
    assert response.status_code == 400
    assert response.json["msg"] == "It's not your vacancy"


def test_delete_vacancy_error(client):
    """
    test `api/vacancies/category_slug` (DELETE) - Create error delete vacancy with not vacancy your
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.delete(f"/api/vacancies/{CATEGORY_SLUG}",
                             headers={"Content-Type": "application/json",
                                      "Authorization": f"Bearer {LOGIN_TOKEN}"},
                             data=json.dumps({"name": 99999}))
    assert response.status_code == 400
    assert response.json["msg"] == "Name of vacancy don't find"
