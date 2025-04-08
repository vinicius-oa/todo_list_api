import jwt
import pytest
from fastapi.testclient import TestClient

from config.di import DI
from config.factory import app
from domain.todo.controllers.auth import AuthController


@pytest.fixture(scope="session")
def di():
    dependencies = DI()
    dependencies.database_driver().setup_database()
    yield


@pytest.fixture(scope="session")
def test_client_one(di):
    client = TestClient(app)
    access_token = jwt.encode({"sub": "teste1"}, AuthController.jwt_sign_secret, AuthController.jwt_sign_alg)
    client.headers = {
        "Authorization": f"Bearer {access_token}",
        **client.headers
    }
    yield client


@pytest.fixture(scope="session")
def test_client_two(di):
    client = TestClient(app)
    access_token = jwt.encode({"sub": "teste2"}, AuthController.jwt_sign_secret, AuthController.jwt_sign_alg)
    client.headers = {
        "Authorization": f"Bearer {access_token}",
        **client.headers
    }
    yield client