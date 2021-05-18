import pytest

from vehicles.api import vehiclesApp as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return flask_app.app.test_client()
