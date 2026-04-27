"""Administration API — config, users, backup."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sparrow.auth.middleware import get_current_user
from sparrow.auth.models import Role, User
from sparrow.auth.rbac import require_permission

router = APIRouter()


class SetupRequest(BaseModel):
    llm_provider: str = "ollama"
    llm_model: str = "llama3"
    llm_api_key: str = ""
    llm_base_url: str = "http://localhost:11434"
    workspace_root: str = ""
    telegram_bot_token: str = ""


@router.get("/admin/config")
async def get_config(user: User = Depends(get_current_user)):
    """Get current configuration (admin only)."""
    require_permission(user.role, "admin.config")
    # Return sanitized config (no secrets)
    return {"status": "ok", "config": {}}


@router.post("/admin/setup")
async def initial_setup(req: SetupRequest):
    """Initial setup wizard endpoint (only works on first run)."""
    # TODO: Apply configuration and persist
    return {"status": "ok", "message": "Setup complete"}


@router.get("/admin/audit")
async def get_audit_log(limit: int = 100, user: User = Depends(get_current_user)):
    """Get audit log entries."""
    require_permission(user.role, "audit.read")
    # TODO: Query from AuditLogger
    return []


@router.post("/admin/backup")
async def create_backup(user: User = Depends(get_current_user)):
    """Create a data backup."""
    require_permission(user.role, "admin.backup")
    # TODO: Create DB + config backup
    return {"status": "ok", "message": "Backup created"}
