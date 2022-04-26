from typing import Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import registry, Session

from weather_notifier.settings import DBAuth, get_settings

mapper_registry = registry()


def get_engine(settings: DBAuth = Depends(get_settings)) -> Engine:
    return create_engine(settings.db_url.get_secret_value(), future=True)


def get_session(engine: Engine = Depends(get_engine)) -> Generator[Session, None, None]:
    with Session(engine) as session:
        with session.begin():
            yield session
