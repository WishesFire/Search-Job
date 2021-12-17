import pytest
import json
from app.models.model import User
from app import create_app, db

app = create_app()


LOGIN_TOKEN = ""
category_slug = "designer"
name = "123123"
salary = 233.0
about = "Good job"
contacts = "+390423423"

email = "lol@mail.com"
password1 = "12345"
password2 = "12345"


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


def test_get_vacancies(client):
    """
    test `/api/vacancies/category_slug` - Get vacancies at slug
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.get(f"/api/vacancies/{category_slug}")
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
        User.query.filter_by(email=email).delete()
        db.session.commit()

    response = client.post("/api/auth/signup", headers={"Content-Type": "application/json"},
                           data=json.dumps({"email": email, "password1": password1, "password2": password2}))

    assert response.status_code == 200
    assert response.json["msg"] == "User successfully created"

    response = client.post("/api/auth/login", headers={"Content-Type": "application/json"},
                           data=json.dumps({"email": email, "password": password1}))
    LOGIN_TOKEN = response.json['token']

    assert response.status_code == 200
    assert response.json["token"] == LOGIN_TOKEN


def test_post_vacancy(client):
    """
    test `api/vacancies/category_slug` (POST) - Create new test vacancy
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.post(f"/api/vacancies/{category_slug}",
                           headers={"Content-Type": "application/json", "Authorization": f"Bearer {LOGIN_TOKEN}"},
                           data=json.dumps({"name": name, "salary": salary, "about": about, "contacts": contacts}))
    assert response.status_code == 200
    assert response.json["msg"] == "New vacancy successfully created"


def test_delete_vacancy(client):
    """
    test `api/vacancies/category_slug` (DELETE) - Delete test vacancy
    :param client: cope app client
    :return: Passed status if code is similar
    """
    response = client.delete(f"/api/vacancies/{category_slug}",
                             headers={"Content-Type": "application/json", "Authorization": f"Bearer {LOGIN_TOKEN}"},
                             data=json.dumps({"name": name}))
    assert response.status_code == 200
    assert response.json["msg"] == f"Vacancy - {name} successfully deleted"
