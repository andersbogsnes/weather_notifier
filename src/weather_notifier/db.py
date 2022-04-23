from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import registry, Session

from weather_notifier.settings import Settings, get_settings

mapper_registry = registry()


def get_engine(settings: Settings = Depends(get_settings)) -> Engine:
    return create_engine(settings.db.db_url.get_secret_value(), future=True)


def get_session(engine: AsyncEngine = Depends(get_engine)) -> Session:
    with Session(engine) as session:
        with session.begin():
            yield session
