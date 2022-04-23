import pytest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from weather_notifier.app import create_app
from weather_notifier.db import mapper_registry
from weather_notifier.settings import Settings, DBAuth, get_settings, APIAuth


@pytest.fixture()
def settings() -> Settings:
    db = DBAuth(db_url="sqlite:///test.db?check_same_thread=False")
    api = APIAuth(api_key="mysecretkey")
    return Settings(db=db, api=api)


@pytest.fixture()
def session(settings: Settings) -> Session:
    engine = create_engine(
        settings.db.db_url.get_secret_value(),
        future=True,
        connect_args={"check_same_thread": False},
    )
    mapper_registry.metadata.create_all(engine)

    with Session(engine) as session:
        with session.begin():
            yield session
            session.rollback()


@pytest.fixture()
def app(settings: Settings) -> FastAPI:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: settings
    return app


@pytest.fixture()
def client(app: FastAPI) -> TestClient:
    return TestClient(app)
