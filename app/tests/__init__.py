import pytest
from app import create_app


app = create_app()


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
