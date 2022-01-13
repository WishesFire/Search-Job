"""
Creates a client object for application testing
"""
# pylint: disable=redefined-outer-name

import pytest
from app import create_app


app = create_app()


@pytest.fixture
def client():
    """
    Create new application as client
    """
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client
