import sqlalchemy as sa
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from weather_notifier.db import get_engine
from weather_notifier.subscriptions.routes import router as subscriptions_router


def index():
    return RedirectResponse("/docs")


def healthcheck(engine: Engine = Depends(get_engine)):
    health_message = {"app": "OK", "db": "OK"}
    try:
        with engine.connect() as conn:
            conn.execute(sa.text("SELECT 1"))
    except SQLAlchemyError:
        return {**health_message, "db": "error"}
    return health_message


def add_default_routes(app: FastAPI) -> FastAPI:
    app.add_route("/", index, methods=["GET"], include_in_schema=False)
    app.add_route("/health", healthcheck, methods=["GET"], include_in_schema=False)

    return app


def create_app() -> FastAPI:
    app = FastAPI(title="Weather Notifier", version="0.1.0")
    app.include_router(subscriptions_router)
    add_default_routes(app)
    return app
