"""Audit log data models."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field

import uuid


class AuditEntry(BaseModel):
    """A single audit log entry."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    user_id: str
    action: str  # e.g., "file.write", "shell.execute"
    target: str = ""  # e.g., file path, command
    parameters: dict[str, Any] = {}
    result: str = ""  # "success" | "denied" | "error"
    details: str = ""
    channel: str = "web"  # Source channel
