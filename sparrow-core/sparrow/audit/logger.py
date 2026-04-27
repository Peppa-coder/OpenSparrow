"""Audit logger — records all operations for accountability."""

from __future__ import annotations

import re
from typing import Any

from sparrow.audit.models import AuditEntry


# Patterns to redact from logs
SECRET_PATTERNS = [
    re.compile(r'(?i)(api[_-]?key|token|secret|password|passwd|auth)\s*[=:]\s*\S+'),
    re.compile(r'(?i)bearer\s+\S+'),
    re.compile(r'sk-[a-zA-Z0-9]{20,}'),
    re.compile(r'ghp_[a-zA-Z0-9]{36}'),
]


def redact_secrets(text: str) -> str:
    """Redact sensitive information from text."""
    for pattern in SECRET_PATTERNS:
        text = pattern.sub("[REDACTED]", text)
    return text


class AuditLogger:
    """Records all operations for audit trail."""

    def __init__(self):
        self._entries: list[AuditEntry] = []

    async def log(self, user_id: str, action: str, target: str = "",
                  parameters: dict[str, Any] | None = None,
                  result: str = "success", details: str = "",
                  channel: str = "web") -> AuditEntry:
        """Record an audit entry."""
        entry = AuditEntry(
            user_id=user_id,
            action=action,
            target=redact_secrets(target),
            parameters={k: redact_secrets(str(v)) for k, v in (parameters or {}).items()},
            result=result,
            details=redact_secrets(details),
            channel=channel,
        )
        self._entries.append(entry)
        # TODO: Persist to SQLite in Phase 2
        return entry

    def get_entries(self, limit: int = 100, user_id: str | None = None,
                    action: str | None = None) -> list[AuditEntry]:
        """Query audit entries with optional filters."""
        entries = self._entries
        if user_id:
            entries = [e for e in entries if e.user_id == user_id]
        if action:
            entries = [e for e in entries if e.action == action]
        return entries[-limit:]

    async def export(self) -> list[dict]:
        """Export all entries as dicts (for backup/download)."""
        return [e.model_dump() for e in self._entries]


# Global logger instance
audit_logger = AuditLogger()
