from fastapi import FastAPI
from weather_notifier.subscriptions.routes import router as subscriptions_router
from importlib import metadata


def create_app() -> FastAPI:
    app = FastAPI(
        title="Weather Notifier", version=metadata.version("weather_notifier")
    )
    app.include_router(subscriptions_router)
    return app
