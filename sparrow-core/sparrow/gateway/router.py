"""Message router — dispatches incoming messages to the agent orchestrator."""

from __future__ import annotations

from typing import Callable, Awaitable

from sparrow.gateway.protocol import UnifiedMessage, UnifiedResponse


class MessageRouter:
    """Routes messages from any channel to the processing pipeline."""

    def __init__(self):
        self._handler: Callable[[UnifiedMessage], Awaitable[UnifiedResponse]] | None = None

    def set_handler(self, handler: Callable[[UnifiedMessage], Awaitable[UnifiedResponse]]):
        """Set the main message handler (typically the agent orchestrator)."""
        self._handler = handler

    async def route(self, message: UnifiedMessage) -> UnifiedResponse:
        """Route an incoming message to the handler."""
        if self._handler is None:
            return UnifiedResponse(content="⚠️ No handler configured. Please complete setup.")
        return await self._handler(message)


# Global router instance
router = MessageRouter()
