"""Risk classification policies for actions."""

from __future__ import annotations

from enum import Enum


class RiskLevel(str, Enum):
    AUTO = "auto"           # Execute immediately, no approval needed
    CONFIRM = "confirm"     # User must confirm
    ADMIN_ONLY = "admin"    # Only admin can approve
    FORBIDDEN = "forbidden" # Never allowed


# Default risk policies for common operations
DEFAULT_POLICIES: dict[str, RiskLevel] = {
    # File operations
    "file.list": RiskLevel.AUTO,
    "file.read": RiskLevel.AUTO,
    "file.write": RiskLevel.CONFIRM,
    "file.search": RiskLevel.AUTO,

    # Shell
    "shell.execute": RiskLevel.CONFIRM,

    # Monitoring
    "monitor.status": RiskLevel.AUTO,

    # Scheduler
    "scheduler.add": RiskLevel.CONFIRM,
    "scheduler.list": RiskLevel.AUTO,
    "scheduler.remove": RiskLevel.CONFIRM,

    # Notifications
    "notify.broadcast": RiskLevel.AUTO,
}

# Commands that are always forbidden
FORBIDDEN_COMMANDS = [
    "rm -rf /",
    "mkfs",
    "dd if=",
    ":(){:|:&};:",
]

# Commands that require admin approval
ADMIN_COMMANDS = [
    "rm -rf",
    "rm -r",
    "git push --force",
    "pip install",
    "npm install -g",
    "apt install",
    "brew install",
    "curl | bash",
    "wget | bash",
]


def classify_command(command: str) -> RiskLevel:
    """Classify a shell command's risk level."""
    cmd_lower = command.lower().strip()

    for pattern in FORBIDDEN_COMMANDS:
        if pattern in cmd_lower:
            return RiskLevel.FORBIDDEN

    for pattern in ADMIN_COMMANDS:
        if pattern in cmd_lower:
            return RiskLevel.ADMIN_ONLY

    return RiskLevel.CONFIRM
