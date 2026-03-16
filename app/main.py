from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api import routes_symptoms
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
    )

    # CORS - permissive for local dev
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Static files
    app.mount(
        "/static",
        StaticFiles(directory="app/static"),
        name="static",
    )

    # Routes
    app.include_router(routes_symptoms.router, prefix="", tags=["symptoms"])

    @app.get("/health")
    async def health():
        return {"status": "ok"}

    return app


app = create_app()

