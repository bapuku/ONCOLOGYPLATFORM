"""OpenAI GPT API client per spec §1 model_registry."""
from typing import Any
from dataclasses import dataclass
import httpx
import structlog

from app.config import get_settings

logger = structlog.get_logger()

GPT_MODELS = {
    "gpt_4o": "gpt-4o-2025-04-09",
    "gpt_5_2": "gpt-5.2-preview",
}

DEFAULT_CONFIGS = {
    "gpt_4o": {"temperature": 0.1, "max_tokens": 16384},
    "gpt_5_2": {"temperature": 0.05, "max_tokens": 32768},
}


@dataclass
class GPTResponse:
    content: str
    model: str
    usage: dict[str, int] | None = None


class GPTClient:
    """OpenAI Chat Completions API client."""

    BASE_URL = "https://api.openai.com/v1/chat/completions"

    def __init__(self, api_key: str | None = None) -> None:
        settings = get_settings()
        self.api_key = api_key or settings.openai_api_key
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(120.0, connect=10.0),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def generate(
        self,
        prompt: str,
        model_key: str = "gpt_4o",
        system: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: str | None = None,
        **kwargs: Any,
    ) -> GPTResponse:
        if not self.api_key:
            return GPTResponse(
                content=self._stub_response(model_key, response_format),
                model=model_key,
            )

        model_id = GPT_MODELS.get(model_key, model_key)
        cfg = DEFAULT_CONFIGS.get(model_key, {})

        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        body: dict[str, Any] = {
            "model": model_id,
            "messages": messages,
            "max_tokens": max_tokens or cfg.get("max_tokens", 8192),
            "temperature": temperature if temperature is not None else cfg.get("temperature", 0.1),
        }
        if response_format == "json":
            body["response_format"] = {"type": "json_object"}

        client = await self._get_client()
        try:
            resp = await client.post(self.BASE_URL, json=body)
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            return GPTResponse(
                content=text,
                model=model_id,
                usage=data.get("usage"),
            )
        except httpx.HTTPStatusError as e:
            logger.error("GPT API error", status=e.response.status_code, body=e.response.text[:500])
            raise
        except Exception as e:
            logger.error("GPT API call failed", error=str(e))
            raise

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    @staticmethod
    def _stub_response(model_key: str, response_format: str | None) -> str:
        if response_format == "json":
            return '{"agent_id":"stub","situation_summary":"No API key configured.","confidence":0.0,"human_oversight_required":true}'
        return f"[{model_key}] No OPENAI_API_KEY configured. Set it in .env for live inference."
