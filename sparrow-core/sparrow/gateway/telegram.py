"""Telegram Bot channel adapter (placeholder for V1)."""

from __future__ import annotations

from sparrow.gateway.protocol import ChannelCapabilities, ChannelType, UnifiedMessage


TELEGRAM_CAPABILITIES = ChannelCapabilities(
    supports_threads=True,
    supports_buttons=True,
    supports_file_upload=True,
    supports_edit=True,
    max_message_length=4096,
)


class TelegramAdapter:
    """Telegram Bot adapter — translates Telegram updates to UnifiedMessage."""

    def __init__(self, bot_token: str, allowed_users: list[str] | None = None):
        self.bot_token = bot_token
        self.allowed_users = allowed_users or []
        self.capabilities = TELEGRAM_CAPABILITIES

    async def start(self):
        """Start polling for Telegram updates. (Implemented in V1 Phase 6)"""
        # TODO: Integrate python-telegram-bot for polling/webhook
        pass

    async def stop(self):
        """Stop the Telegram bot."""
        pass

    def _to_unified(self, update: dict) -> UnifiedMessage:
        """Convert a Telegram update to UnifiedMessage."""
        # Placeholder — will parse telegram.Update in full implementation
        return UnifiedMessage(
            channel=ChannelType.TELEGRAM,
            user_id=str(update.get("from", {}).get("id", "")),
            user_name=update.get("from", {}).get("username", ""),
            content=update.get("text", ""),
        )
