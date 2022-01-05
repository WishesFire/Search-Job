from . import client, app

STATUS_CODE = 200


def test_config():
    """
    Check application config
    :param client: copy app client
    :return: Passed status if code is similar
    """
    assert app.config["DEBUG"]
    assert app.config["SECRET_KEY"]
    assert app.config["DB_USERNAME"]
    assert app.config["DB_PASSWORD"]
    assert app.config["DB_NAME"]


def test_status_main(client):
    """
    Check get main page
    / - main_page
    :param client: copy app client
    :return: Passed status if code is similar
    """
    res = client.get("/")
    assert STATUS_CODE == res.status_code
