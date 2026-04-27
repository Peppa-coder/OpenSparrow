"""Tasks and approval queue API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sparrow.auth.middleware import get_current_user
from sparrow.auth.models import User

router = APIRouter()


@router.get("/tasks/pending")
async def list_pending_approvals(user: User = Depends(get_current_user)):
    """List pending approval requests."""
    # TODO: Connect to ApprovalEngine
    return []


@router.post("/tasks/{task_id}/approve")
async def approve_task(task_id: str, user: User = Depends(get_current_user)):
    """Approve a pending task."""
    # TODO: Connect to ApprovalEngine
    return {"task_id": task_id, "status": "approved"}


@router.post("/tasks/{task_id}/reject")
async def reject_task(task_id: str, user: User = Depends(get_current_user)):
    """Reject a pending task."""
    # TODO: Connect to ApprovalEngine
    return {"task_id": task_id, "status": "rejected"}


@router.get("/tasks/history")
async def task_history(limit: int = 50, user: User = Depends(get_current_user)):
    """Get task execution history."""
    # TODO: Query from DB
    return []
