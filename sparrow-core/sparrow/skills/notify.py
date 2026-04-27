"""Notification skill — broadcast messages to team channels."""

from __future__ import annotations

from sparrow.skills.registry import SkillDef


async def broadcast(message: str, channels: list[str] | None = None, **kwargs) -> dict:
    """Broadcast a message to one or more channels."""
    return {"action": "notify.broadcast", "message": message, "channels": channels or ["all"]}


NOTIFY_SKILLS = [
    SkillDef(name="notify.broadcast", description="Send a notification to team channels", handler=broadcast, risk_level="low"),
]
