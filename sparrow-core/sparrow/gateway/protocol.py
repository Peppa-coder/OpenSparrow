"""Unified message protocol for cross-channel communication."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field

import uuid


class ChannelType(str, Enum):
    WEB = "web"
    TELEGRAM = "telegram"
    SLACK = "slack"
    WEBHOOK = "webhook"


class Attachment(BaseModel):
    filename: str
    content_type: str
    url: str = ""
    size: int = 0


class Action(BaseModel):
    """Interactive action (button, quick reply)."""
    id: str
    label: str
    action_type: str = "button"  # "button" | "link"
    value: str = ""


class UnifiedMessage(BaseModel):
    """Platform-agnostic message representation."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    channel: ChannelType
    user_id: str
    user_name: str = ""
    thread_id: Optional[str] = None
    content: str
    attachments: list[Attachment] = []
    actions: list[Action] = []
    metadata: dict[str, Any] = {}  # Channel-specific data passthrough
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class UnifiedResponse(BaseModel):
    """Response to send back through a channel."""
    content: str
    attachments: list[Attachment] = []
    actions: list[Action] = []
    reply_to: Optional[str] = None  # thread_id


class ChannelCapabilities(BaseModel):
    """Declares what a channel adapter supports."""
    supports_threads: bool = False
    supports_buttons: bool = False
    supports_file_upload: bool = False
    supports_edit: bool = False
    max_message_length: int = 4096
