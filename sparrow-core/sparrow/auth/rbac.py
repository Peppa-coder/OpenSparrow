"""Role-based access control."""

from __future__ import annotations

from typing import Any

from sparrow.auth.models import Role

# Permission matrix: role -> allowed actions
PERMISSIONS: dict[Role, set[str]] = {
    Role.ADMIN: {
        "files.read", "files.write", "files.delete",
        "shell.execute", "shell.execute_dangerous",
        "tasks.create", "tasks.approve", "tasks.cancel",
        "admin.config", "admin.users", "admin.backup",
        "monitor.read", "audit.read",
    },
    Role.MEMBER: {
        "files.read", "files.write",
        "shell.execute",
        "tasks.create",
        "monitor.read",
    },
    Role.VIEWER: {
        "files.read",
        "monitor.read",
        "audit.read",
    },
}


def has_permission(role: Role, action: str) -> bool:
    """Check if a role has permission for an action."""
    return action in PERMISSIONS.get(role, set())


def require_permission(role: Role, action: str) -> None:
    """Raise if role lacks permission."""
    if not has_permission(role, action):
        raise PermissionError(f"Role '{role}' lacks permission for '{action}'")
