"""Skill registry — discover, register, and invoke skills."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Awaitable


@dataclass
class SkillDef:
    """Definition of a registered skill."""
    name: str
    description: str
    handler: Callable[..., Awaitable[Any]]
    risk_level: str = "low"  # "low" | "medium" | "high" | "critical"
    parameters: dict[str, Any] = field(default_factory=dict)


class SkillRegistry:
    """Central registry for all available skills."""

    def __init__(self):
        self._skills: dict[str, SkillDef] = {}

    def register(self, skill: SkillDef):
        """Register a skill."""
        self._skills[skill.name] = skill

    def get(self, name: str) -> SkillDef | None:
        """Get a skill by name."""
        return self._skills.get(name)

    def list_skills(self) -> list[SkillDef]:
        """List all registered skills."""
        return list(self._skills.values())

    def list_for_llm(self) -> list[dict]:
        """Return skill definitions formatted for LLM function calling."""
        return [
            {
                "name": s.name,
                "description": s.description,
                "risk_level": s.risk_level,
                "parameters": s.parameters,
            }
            for s in self._skills.values()
        ]


# Global registry
registry = SkillRegistry()
