from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings


def add_cors_middleware(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=settings.cors.credentials,
        allow_methods=settings.cors.methods,
        allow_headers=settings.cors.headers,
    )
    return app
