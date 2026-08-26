"""Application entry point: `uvicorn app.main:app`, or `just backend dev`."""

from fastapi import FastAPI

from app.api import health
from app.config import Settings
from app.spa import register_spa


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build a FastAPI application.

    A factory rather than a module-level singleton, so tests can point an app
    at a throwaway directory without a real frontend build existing.
    """
    settings = settings or Settings.from_env()

    app = FastAPI(
        title="Meal Planner",
        # The defaults (/docs, /openapi.json, /docs/oauth2-redirect) sit
        # outside /api and could collide with a future client-side route.
        docs_url="/api/docs",
        redoc_url=None,
        openapi_url="/api/openapi.json",
        swagger_ui_oauth2_redirect_url="/api/docs/oauth2-redirect",
    )

    app.include_router(health.router, prefix="/api")

    # Last: its catch-all matches every remaining path.
    register_spa(app, settings.static_dir)

    return app


app = create_app()
