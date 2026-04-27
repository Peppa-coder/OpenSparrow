"""Anthropic Claude LLM adapter."""

from __future__ import annotations

import httpx

from sparrow.llm.base import BaseLLM, LLMMessage, LLMResponse


class AnthropicAdapter(BaseLLM):
    """Adapter for Anthropic Claude API."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.anthropic.com/v1"

    async def chat(self, messages: list[LLMMessage], **kwargs) -> LLMResponse:
        system_msg = ""
        chat_messages = []
        for m in messages:
            if m.role == "system":
                system_msg = m.content
            else:
                chat_messages.append({"role": m.role, "content": m.content})

        async with httpx.AsyncClient(timeout=60) as client:
            body = {
                "model": self.model,
                "max_tokens": kwargs.get("max_tokens", 4096),
                "messages": chat_messages,
            }
            if system_msg:
                body["system"] = system_msg

            resp = await client.post(
                f"{self.base_url}/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json=body,
            )
            resp.raise_for_status()
            data = resp.json()
            return LLMResponse(
                content=data["content"][0]["text"],
                model=data.get("model", self.model),
                usage=data.get("usage", {}),
            )

    async def health_check(self) -> bool:
        # Anthropic doesn't have a /models endpoint; just verify connectivity
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get("https://api.anthropic.com/v1/models",
                    headers={"x-api-key": self.api_key, "anthropic-version": "2023-06-01"})
                return resp.status_code in (200, 401)  # 401 means reachable but bad key
        except Exception:
            return False
