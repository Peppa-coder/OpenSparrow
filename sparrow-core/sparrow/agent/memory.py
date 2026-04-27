"""Simple conversation memory for the agent."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MemoryEntry:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


class ConversationMemory:
    """Per-user conversation memory with a sliding window."""

    def __init__(self, max_turns: int = 20):
        self.max_turns = max_turns
        self._conversations: dict[str, list[MemoryEntry]] = defaultdict(list)

    def add(self, user_id: str, role: str, content: str):
        """Add a message to the conversation."""
        conv = self._conversations[user_id]
        conv.append(MemoryEntry(role=role, content=content))
        # Trim to max_turns (keep system message if present)
        if len(conv) > self.max_turns:
            self._conversations[user_id] = conv[-self.max_turns:]

    def get_history(self, user_id: str) -> list[dict]:
        """Get conversation history formatted for LLM."""
        return [
            {"role": e.role, "content": e.content}
            for e in self._conversations[user_id]
        ]

    def clear(self, user_id: str):
        """Clear a user's conversation history."""
        self._conversations.pop(user_id, None)
