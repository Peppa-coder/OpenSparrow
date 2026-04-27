"""System monitoring skill — CPU, memory, disk status."""

from __future__ import annotations

from sparrow.skills.registry import SkillDef


async def system_status(**kwargs) -> dict:
    """Get current system resource usage."""
    return {"action": "monitor.status"}


MONITOR_SKILLS = [
    SkillDef(name="monitor.status", description="Get CPU, memory, and disk usage", handler=system_status, risk_level="low"),
]
