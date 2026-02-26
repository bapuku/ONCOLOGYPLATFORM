"""IBM Granite on-premise client per spec §1 model_registry.
Deployed on-premise for GDPR-sensitive workloads. No data leaves hospital infrastructure.
"""
from typing import Any
from dataclasses import dataclass
import httpx
import structlog

from app.config import get_settings

logger = structlog.get_logger()


@dataclass
class GraniteResponse:
    content: str
    model: str
    usage: dict[str, int] | None = None


class GraniteClient:
    """IBM Granite on-premise inference. Connects to local Triton/vLLM endpoint."""

    def __init__(self, base_url: str | None = None) -> None:
        settings = get_settings()
        self.base_url = base_url or getattr(settings, "granite_endpoint", "http://localhost:8001/v1/chat/completions")
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                timeout=httpx.Timeout(60.0, connect=5.0),
                headers={"Content-Type": "application/json"},
            )
        return self._client

    async def generate(
        self,
        prompt: str,
        model_key: str = "ibm_granite_3_1_8b_instruct",
        system: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        response_format: str | None = None,
        **kwargs: Any,
    ) -> GraniteResponse:
        """Generate via on-premise Granite. Falls back to stub if endpoint unavailable."""
        messages: list[dict[str, str]] = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        body: dict[str, Any] = {
            "model": "ibm/granite-3.1-8b-instruct",
            "messages": messages,
            "max_tokens": max_tokens or 8192,
            "temperature": temperature if temperature is not None else 0.1,
        }

        client = await self._get_client()
        try:
            resp = await client.post(self.base_url, json=body)
            resp.raise_for_status()
            data = resp.json()
            text = data["choices"][0]["message"]["content"]
            return GraniteResponse(content=text, model="ibm/granite-3.1-8b-instruct", usage=data.get("usage"))
        except Exception as e:
            logger.warning("Granite on-premise unavailable, returning stub", error=str(e))
            stub = '{"agent_id":"stub","situation_summary":"On-premise Granite unavailable.","confidence":0.0,"human_oversight_required":true}'
            return GraniteResponse(
                content=stub if response_format == "json" else "On-premise Granite unavailable.",
                model="ibm/granite-3.1-8b-instruct",
            )

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
