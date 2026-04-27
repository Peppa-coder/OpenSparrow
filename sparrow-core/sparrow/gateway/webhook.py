"""Generic Webhook channel adapter."""

from __future__ import annotations

from sparrow.gateway.protocol import ChannelCapabilities, ChannelType, UnifiedMessage


WEBHOOK_CAPABILITIES = ChannelCapabilities(
    supports_threads=False,
    supports_buttons=False,
    supports_file_upload=True,
    supports_edit=False,
    max_message_length=65536,
)


class WebhookAdapter:
    """Generic webhook adapter for custom integrations."""

    capabilities = WEBHOOK_CAPABILITIES

    @staticmethod
    def parse_incoming(payload: dict) -> UnifiedMessage:
        """Parse an incoming webhook payload to UnifiedMessage."""
        return UnifiedMessage(
            channel=ChannelType.WEBHOOK,
            user_id=payload.get("user_id", "webhook"),
            user_name=payload.get("user_name", "Webhook"),
            content=payload.get("content", payload.get("text", "")),
            metadata=payload,
        )
