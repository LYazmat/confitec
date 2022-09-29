import pytest
from app import create_app

@pytest.fixture(scope='module')
def app():
    return create_app()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()