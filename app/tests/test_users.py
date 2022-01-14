"""
Testing is related to the interaction with users functions
"""
# pylint: disable=redefined-outer-name
# pylint: disable=unused-import

from werkzeug.security import generate_password_hash
from app.configs.config import InitTestDataDB
from app.service.user_service import UserService
from . import client, app


STATUS_CODE = 200


def before_user_access(flag):
    """
    Check user exists
    """
    with app.app_context():
        if flag:
            result = UserService.find_user_by_email(InitTestDataDB.USER_EMAIL)
            if not result:
                secure_password = generate_password_hash(InitTestDataDB.USER_PASSWORD,
                                                         method="sha256")
                UserService.create_new_user(InitTestDataDB.USER_EMAIL, secure_password)
        else:
            result = UserService.find_user_by_email(InitTestDataDB.USER_EMAIL)
            if result:
                UserService.delete_user(InitTestDataDB.USER_EMAIL)


def after_user_delete():
    """
    Delete user after test
    """
    with app.app_context():
        UserService.delete_user(InitTestDataDB.USER_EMAIL)


def test_create_user_db():
    """
    Check creating user through the database
    """
    with app.app_context():
        result = UserService.find_user_by_email(InitTestDataDB.USER_EMAIL)
        if result:
            UserService.delete_user(InitTestDataDB.USER_EMAIL)
        secure_password = generate_password_hash(InitTestDataDB.USER_PASSWORD, method="sha256")
        UserService.create_new_user(InitTestDataDB.USER_EMAIL, secure_password)
        result = UserService.find_user_by_email(InitTestDataDB.USER_EMAIL)
        assert result.email == InitTestDataDB.USER_EMAIL
        UserService.delete_user(InitTestDataDB.USER_EMAIL)


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
    res = client.post("/login", data={"emailAddress": InitTestDataDB.USER_EMAIL,
                                      "password": InitTestDataDB.USER_PASSWORD},
                      follow_redirects=True)
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
    client.post("/signup", data=dict(emailAddress=InitTestDataDB.USER_EMAIL,
                                     password1=InitTestDataDB.USER_PASSWORD,
                                     password2=InitTestDataDB.USER_PASSWORD))

    result = UserService.find_user_by_email(InitTestDataDB.USER_EMAIL)
    assert result.email == InitTestDataDB.USER_EMAIL

    after_user_delete()


def test_profile(client):
    """
    Check GET profile
    :param client: copy app client
    :return: Passed status if code is similar
    """
    res = client.get("/profile", follow_redirects=True)
    assert res.status_code == STATUS_CODE


def test_profile_delete(client):
    """
    Check DELETE profile
    :param client: copy app client
    :return: Passed status if code is similar
    """
    res = client.delete("/profile", follow_redirects=True, data={"name": "1111"})
    assert res.status_code == STATUS_CODE
