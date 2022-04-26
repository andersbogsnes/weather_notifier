from fastapi import FastAPI

from weather_notifier.subscriptions.routes import router as subscriptions_router


def create_app() -> FastAPI:
    app = FastAPI(title="Weather Notifier", version="0.1.0")
    app.include_router(subscriptions_router)
    return app
