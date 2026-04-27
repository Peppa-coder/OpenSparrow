"""Scheduler skill — cron-like task scheduling."""

from __future__ import annotations

from sparrow.skills.registry import SkillDef


async def schedule_task(cron: str, command: str, name: str = "", **kwargs) -> dict:
    """Schedule a recurring task."""
    return {"action": "scheduler.add", "cron": cron, "command": command, "name": name}


async def list_scheduled(**kwargs) -> dict:
    """List all scheduled tasks."""
    return {"action": "scheduler.list"}


async def remove_scheduled(task_id: str, **kwargs) -> dict:
    """Remove a scheduled task."""
    return {"action": "scheduler.remove", "task_id": task_id}


SCHEDULER_SKILLS = [
    SkillDef(name="scheduler.add", description="Schedule a recurring task with cron expression", handler=schedule_task, risk_level="medium"),
    SkillDef(name="scheduler.list", description="List all scheduled tasks", handler=list_scheduled, risk_level="low"),
    SkillDef(name="scheduler.remove", description="Remove a scheduled task", handler=remove_scheduled, risk_level="medium"),
]
