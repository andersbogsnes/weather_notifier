from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.engine import Engine

import sqlalchemy as sa
from sqlalchemy.exc import SQLAlchemyError
from weather_notifier.db import get_session, get_engine
from weather_notifier.subscriptions.routes import router as subscriptions_router


def create_app() -> FastAPI:
    app = FastAPI(title="Weather Notifier", version="0.1.0")
    app.include_router(subscriptions_router)

    @app.get("/", include_in_schema=False)
    def index():
        return RedirectResponse("/docs")

    @app.get("/health", include_in_schema=False)
    def healthcheck(engine: Engine = Depends(get_engine)):
        health_message = {
            "app": "OK",
            "db": "OK"
        }
        try:
            with engine.connect() as conn:
                conn.execute(sa.text("SELECT 1"))
        except SQLAlchemyError:
            return {**health_message, "db": "error"}
        return health_message

    return app
