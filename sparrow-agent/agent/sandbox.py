"""Security sandbox — path validation and execution constraints."""

from __future__ import annotations

import os
from pathlib import Path


class SandboxViolation(Exception):
    """Raised when an operation violates sandbox constraints."""
    pass


class Sandbox:
    """Enforces workspace boundaries and execution safety."""

    def __init__(self, workspace_root: str):
        self.workspace_root = Path(workspace_root).expanduser().resolve()
        self._ensure_workspace()

    def _ensure_workspace(self):
        """Create workspace directory if it doesn't exist."""
        self.workspace_root.mkdir(parents=True, exist_ok=True)

    def validate_path(self, path: str) -> Path:
        """Validate and resolve a path within the workspace.

        Prevents path traversal attacks (e.g., ../../etc/passwd).
        """
        # Resolve the path relative to workspace
        if os.path.isabs(path):
            resolved = Path(path).resolve()
        else:
            resolved = (self.workspace_root / path).resolve()

        # Check that the resolved path is within workspace
        try:
            resolved.relative_to(self.workspace_root)
        except ValueError:
            raise SandboxViolation(
                f"Access denied: '{path}' is outside the workspace boundary "
                f"({self.workspace_root})"
            )

        return resolved

    def is_safe_command(self, command: str) -> tuple[bool, str]:
        """Check if a command is safe to execute.

        Returns (is_safe, reason).
        """
        dangerous_patterns = [
            ("rm -rf /", "Attempted to delete root filesystem"),
            ("mkfs", "Attempted to format a filesystem"),
            (":(){:|:&};:", "Fork bomb detected"),
            ("dd if=/dev/zero", "Dangerous disk operation"),
            ("> /dev/sd", "Direct device write"),
        ]

        cmd_lower = command.lower().strip()
        for pattern, reason in dangerous_patterns:
            if pattern in cmd_lower:
                return False, reason

        return True, "ok"
