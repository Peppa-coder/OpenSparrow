"""Shell execution skill — guarded command execution on the work machine."""

from __future__ import annotations

from sparrow.skills.registry import SkillDef


async def execute_command(command: str, **kwargs) -> dict:
    """Execute a shell command (subject to approval)."""
    return {"action": "shell.execute", "command": command}


SHELL_SKILLS = [
    SkillDef(
        name="shell.execute",
        description="Execute a shell command on the work machine",
        handler=execute_command,
        risk_level="high",
        parameters={"command": {"type": "string", "description": "The shell command to execute"}},
    ),
]
