import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from weather_notifier.app import create_app
from weather_notifier.settings import DBAuth, get_settings


@pytest.fixture(scope="session")
def settings() -> DBAuth:
    return DBAuth(db_url="sqlite:///")


@pytest.fixture(scope="session")
def app(settings: DBAuth) -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    return app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
