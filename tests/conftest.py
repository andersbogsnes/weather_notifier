import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from weather_notifier.app import create_app
from weather_notifier.settings import Settings, DBAuth, get_settings, APIAuth


@pytest.fixture(scope="session")
def settings() -> Settings:
    db = DBAuth(db_url="sqlite:///")
    api = APIAuth(api_key="mysecretkey")
    return Settings(db=db, api=api)


@pytest.fixture(scope="session")
def app(settings: Settings) -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    return app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
