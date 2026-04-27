"""File management REST API."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from sparrow.auth.middleware import get_current_user
from sparrow.auth.models import User

router = APIRouter()


class FileInfo(BaseModel):
    name: str
    path: str
    is_dir: bool
    size: int = 0


class WriteFileRequest(BaseModel):
    path: str
    content: str


@router.get("/files", response_model=list[FileInfo])
async def list_files(path: str = ".", user: User = Depends(get_current_user)):
    """List files in the workspace directory."""
    # TODO: Delegate to local agent via WebSocket
    return []


@router.get("/files/read")
async def read_file(path: str, user: User = Depends(get_current_user)):
    """Read a file's content from the workspace."""
    # TODO: Delegate to local agent
    return {"path": path, "content": "", "status": "not_implemented"}


@router.post("/files/write")
async def write_file(req: WriteFileRequest, user: User = Depends(get_current_user)):
    """Write content to a file in the workspace."""
    # TODO: Delegate to local agent + approval check
    return {"path": req.path, "status": "not_implemented"}
