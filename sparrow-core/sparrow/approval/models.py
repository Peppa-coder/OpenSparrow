"""Approval request data models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

import uuid


class ApprovalStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class ApprovalRequest(BaseModel):
    """A request for human approval before executing a risky action."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    skill_name: str
    description: str
    parameters: dict = {}
    risk_level: str = "high"
    requested_by: str = ""
    status: ApprovalStatus = ApprovalStatus.PENDING
    reviewed_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    reviewed_at: Optional[datetime] = None
