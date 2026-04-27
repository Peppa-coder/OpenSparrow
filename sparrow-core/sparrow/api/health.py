"""Health check API."""

from __future__ import annotations

from fastapi import APIRouter

from sparrow import __version__

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return {
        "status": "ok",
        "version": __version__,
        "service": "opensparrow-core",
    }


@router.get("/health/detailed")
async def detailed_health():
    """Detailed health check including subsystem status."""
    # TODO: Check LLM, agent connection, DB status
    return {
        "status": "ok",
        "version": __version__,
        "subsystems": {
            "database": "ok",
            "llm": "unconfigured",
            "agent": "disconnected",
            "telegram": "unconfigured",
        },
    }
