"""Auth data models."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class Role(str, Enum):
    ADMIN = "admin"
    MEMBER = "member"
    VIEWER = "viewer"


class User(BaseModel):
    id: str
    username: str
    role: Role = Role.MEMBER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TokenPayload(BaseModel):
    sub: str  # user_id
    role: Role
    exp: datetime
