import pytest
from app import create_app, db
from werkzeug.security import generate_password_hash
from app.configs.config import InitTestDataDB
from app.models.model import User


STATUS_CODE = 200

app = create_app()


@pytest.fixture
def created_test_db():
    """
    Create app context for db operations
    """
    app.config["TESTING"] = True
    with app.app_context() as created_db:
        yield created_db


@pytest.fixture
def client():
    """
    Create new application as client
    :return: copy app client
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def before_user_access(flag):
    """
    Check user exists
    """
    with app.app_context():
        if flag:
            result = User.query.filter_by(email=InitTestDataDB.USER_EMAIL).first()
            if not result:
                secure_password = generate_password_hash(InitTestDataDB.USER_PASSWORD, method="sha256")
                new_user = User(email=InitTestDataDB.USER_EMAIL, password=secure_password)
                db.session.add(new_user)
                db.session.commit()
        else:
            result = User.query.filter_by(email=InitTestDataDB.USER_EMAIL).first()
            if result:
                User.query.filter_by(email=InitTestDataDB.USER_EMAIL).delete()


def after_user_delete():
    """
    Delete user after test
    """
    with app.app_context():
        User.query.filter_by(email=InitTestDataDB.USER_EMAIL).delete()


def test_create_user_db(created_test_db):
    """
    Check creating user through the database
    """
    with app.app_context():
        result = User.query.filter_by(email=InitTestDataDB.USER_EMAIL).first()
        if result:
            User.query.filter_by(email=InitTestDataDB.USER_EMAIL).delete()

        secure_password = generate_password_hash(InitTestDataDB.USER_PASSWORD, method="sha256")
        new_user = User(email=InitTestDataDB.USER_EMAIL, password=secure_password)
        db.session.add(new_user)
        db.session.commit()

        result = User.query.filter_by(email=InitTestDataDB.USER_EMAIL).first()
        assert result.email == InitTestDataDB.USER_EMAIL

        User.query.filter_by(email=InitTestDataDB.USER_EMAIL).delete()


def test_get_login_user(client):
    """
    Check GET login in user
    /login - login user
    :param client: copy app client
    :return: Passed status if code is similar
    """
    res = client.get("/login")
    assert res.status_code == STATUS_CODE


def test_post_login_user(client):
    """
    Check POST login in user
    /login - login user
    :param client:
    :return:
    """
    before_user_access(flag=True)
    client.post("/login", data=dict(emailAddress=InitTestDataDB.USER_EMAIL, password=InitTestDataDB.USER_PASSWORD))
    res = client.get("/profile")
    assert res.status_code == STATUS_CODE

    after_user_delete()


def test_get_sign_up_user(client):
    """
    Check GET registration user
    /signup - registration new user
    :param client: copy app client
    :return: Passed status if code is similar
    """
    res = client.get("/signup")
    assert res.status_code == STATUS_CODE


def test_post_sign_up_user(client):
    """
    Check POST registration user
    /signup - registration new user
    :param client: copy app client
    :return: Passed status if code is similar
    """
    before_user_access(flag=False)
    client.post("/signup", data=dict(emailAddress=InitTestDataDB.USER_EMAIL, password1=InitTestDataDB.USER_PASSWORD,
                                     password2=InitTestDataDB.USER_PASSWORD))

    result = User.query.filter_by(email=InitTestDataDB.USER_EMAIL).first()
    assert result.email == InitTestDataDB.USER_EMAIL

    after_user_delete()


def test_create_vacancy():
    """
    Check create new vacancy using a user profile
    """
    pass
