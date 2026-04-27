"""OpenSparrow Core — FastAPI application entry point."""

from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sparrow import __version__
from sparrow.config import load_config
from sparrow.db.database import Database
from sparrow.api import chat, files, tasks, admin, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown."""
    config = load_config()
    app.state.config = config

    # Initialize database
    db = Database(config.db_path)
    await db.initialize()
    app.state.db = db

    print(f"🐦 OpenSparrow Core v{__version__} starting on {config.host}:{config.port}")
    print(f"   Workspace: {config.workspace_root}")
    print(f"   LLM: {config.llm_provider}/{config.llm_model}")

    yield

    await db.close()
    print("🐦 OpenSparrow Core shutting down")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="OpenSparrow",
        description="🐦 Lightweight AI agent for small teams",
        version=__version__,
        lifespan=lifespan,
    )

    config = load_config()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(health.router, prefix="/api", tags=["health"])
    app.include_router(chat.router, prefix="/api", tags=["chat"])
    app.include_router(files.router, prefix="/api", tags=["files"])
    app.include_router(tasks.router, prefix="/api", tags=["tasks"])
    app.include_router(admin.router, prefix="/api", tags=["admin"])

    return app


app = create_app()


def cli_entry():
    """CLI entry point for sparrow-core."""
    import uvicorn

    config = load_config()
    uvicorn.run(
        "sparrow.main:app",
        host=config.host,
        port=config.port,
        reload=config.debug,
    )


if __name__ == "__main__":
    cli_entry()
