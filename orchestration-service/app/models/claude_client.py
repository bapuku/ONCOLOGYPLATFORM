"""Anthropic Claude API client per spec §1 model_registry."""
from typing import Any
from dataclasses import dataclass
import httpx
import structlog

from app.config import get_settings

logger = structlog.get_logger()

CLAUDE_MODELS = {
    "claude_opus_4": "claude-opus-4-20250514",
    "claude_sonnet_4": "claude-sonnet-4-20250514",
    "claude_4_5_sonnet": "claude-4-5-sonnet-20250514",
}

DEFAULT_CONFIGS = {
    "claude_opus_4": {"temperature": 0.1, "max_tokens": 32768, "top_p": 0.95},
    "claude_sonnet_4": {"temperature": 0.2, "max_tokens": 16384, "top_p": 0.9},
    "claude_4_5_sonnet": {"temperature": 0.05, "max_tokens": 8192},
}


@dataclass
class ClaudeResponse:
    content: str
    model: str
    usage: dict[str, int] | None = None
    stop_reason: str | None = None


class ClaudeClient:
    """Anthropic Messages API client. Uses httpx for async calls."""

    BASE_URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"

    def __init__(self, api_key: str | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.anthropic_api_key
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(120.0, connect=10.0),
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": self.API_VERSION,
                    "content-type": "application/json",
                },
            )
        return self._client

    async def generate(
        self,
        prompt: str,
        model_key: str = "claude_opus_4",
        system: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: str | None = None,
        extended_thinking: bool = False,
        **kwargs: Any,
    ) -> ClaudeResponse:
        if not self.api_key:
            return ClaudeResponse(
                content=self._stub_response(model_key, response_format),
                model=model_key,
            )

        model_id = CLAUDE_MODELS.get(model_key, model_key)
        cfg = DEFAULT_CONFIGS.get(model_key, {})

        messages = [{"role": "user", "content": prompt}]
        body: dict[str, Any] = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens or cfg.get("max_tokens", 8192),
        }
        if system:
            body["system"] = system
        if temperature is not None:
            body["temperature"] = temperature
        elif "temperature" in cfg:
            body["temperature"] = cfg["temperature"]

        client = await self._get_client()
        try:
            resp = await client.post(self.BASE_URL, json=body)
            resp.raise_for_status()
            data = resp.json()
            text = ""
            for block in data.get("content", []):
                if block.get("type") == "text":
                    text += block["text"]
            return ClaudeResponse(
                content=text,
                model=model_id,
                usage=data.get("usage"),
                stop_reason=data.get("stop_reason"),
            )
        except httpx.HTTPStatusError as e:
            logger.error("Claude API error", status=e.response.status_code, body=e.response.text[:500])
            raise
        except Exception as e:
            logger.error("Claude API call failed", error=str(e))
            raise

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    @staticmethod
    def _stub_response(model_key: str, response_format: str | None) -> str:
        if response_format == "json":
            return '{"agent_id":"stub","situation_summary":"No API key configured.","confidence":0.0,"human_oversight_required":true}'
        return f"[{model_key}] No ANTHROPIC_API_KEY configured. Set it in .env for live inference."
