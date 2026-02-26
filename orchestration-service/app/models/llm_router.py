"""LLM router - selects model per task per model_registry rules (YAML §1).
Routes to Claude, GPT, Mistral, or Granite based on task type and complexity.
"""
from typing import Any
from dataclasses import dataclass
import structlog

from app.models.claude_client import ClaudeClient
from app.models.gpt_client import GPTClient
from app.models.mistral_client import MistralClient
from app.models.granite_client import GraniteClient

logger = structlog.get_logger()

TASK_TYPE_TO_MODEL = {
    "orchestration": "claude_opus_4",
    "complex_clinical_reasoning": "claude_opus_4",
    "hypothesis_generation": "claude_opus_4",
    "patient_communication": "claude_sonnet_4",
    "literature": "claude_sonnet_4",
    "report_generation": "claude_sonnet_4",
    "mental_health": "claude_sonnet_4",
    "palliative_care": "claude_sonnet_4",
    "ethics_compliance_check": "claude_4_5_sonnet",
    "bias_detection": "claude_4_5_sonnet",
    "image_analysis": "gpt_4o",
    "multimodal": "gpt_4o",
    "scientific_reasoning": "gpt_5_2",
    "drug_discovery": "gpt_5_2",
    "genomic_interpretation": "gpt_5_2",
    "trial_matching": "mistral_large",
    "guideline_interpretation": "mistral_large",
    "european_guidelines": "mistral_large",
    "structured_extraction": "ibm_granite_3_1_8b_instruct",
    "privacy_sensitive": "ibm_granite_3_1_8b_instruct",
    "default": "claude_sonnet_4",
}

PROVIDER_MAP = {
    "claude_opus_4": "anthropic",
    "claude_sonnet_4": "anthropic",
    "claude_4_5_sonnet": "anthropic",
    "gpt_4o": "openai",
    "gpt_5_2": "openai",
    "mistral_large": "mistral",
    "ibm_granite_3_1_8b_instruct": "granite",
}


@dataclass
class LLMResponse:
    content: str
    model_id: str
    usage: dict[str, int] | None = None


class LLMRouter:
    """Routes requests to the appropriate foundation model per platform spec."""

    def __init__(self) -> None:
        self.claude = ClaudeClient()
        self.gpt = GPTClient()
        self.mistral = MistralClient()
        self.granite = GraniteClient()

    def route(self, task_type: str | None = None, complexity: float = 0.5, **kwargs: Any) -> str:
        """Return model key for the task based on routing rules."""
        if task_type and task_type in TASK_TYPE_TO_MODEL:
            model = TASK_TYPE_TO_MODEL[task_type]
        elif complexity > 0.8:
            model = "claude_opus_4"
        else:
            model = TASK_TYPE_TO_MODEL["default"]
        return model

    async def generate(
        self,
        prompt: str,
        model_id: str = "claude_opus_4",
        system: str | None = None,
        extended_thinking: bool = False,
        response_format: str | None = None,
        task_type: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        resolved = model_id if model_id in PROVIDER_MAP else self.route(task_type)
        provider = PROVIDER_MAP.get(resolved, "anthropic")

        logger.info("llm_router.generate", model=resolved, provider=provider, task_type=task_type)

        try:
            if provider == "anthropic":
                resp = await self.claude.generate(
                    prompt=prompt, model_key=resolved, system=system,
                    response_format=response_format, extended_thinking=extended_thinking, **kwargs,
                )
            elif provider == "openai":
                resp = await self.gpt.generate(
                    prompt=prompt, model_key=resolved, system=system,
                    response_format=response_format, **kwargs,
                )
            elif provider == "mistral":
                resp = await self.mistral.generate(
                    prompt=prompt, model_key=resolved, system=system,
                    response_format=response_format, **kwargs,
                )
            elif provider == "granite":
                resp = await self.granite.generate(
                    prompt=prompt, model_key=resolved, system=system,
                    response_format=response_format, **kwargs,
                )
            else:
                resp = await self.claude.generate(
                    prompt=prompt, model_key=resolved, system=system,
                    response_format=response_format, **kwargs,
                )
            return LLMResponse(content=resp.content, model_id=resp.model, usage=resp.usage)
        except Exception as e:
            logger.error("LLM generation failed, falling back to stub", error=str(e), model=resolved)
            return self._fallback_response(resolved, response_format)

    def _fallback_response(self, model_id: str, response_format: str | None) -> LLMResponse:
        if response_format == "json":
            content = '{"agent_id":"OrchestrationAgent","situation_summary":"LLM unavailable. Configure API keys.","confidence":0.0,"human_oversight_required":true,"json_metrics":null,"vocal_summary":null}'
        else:
            content = "LLM unavailable. Configure API keys in .env for live inference."
        return LLMResponse(content=content, model_id=model_id)

    async def close(self) -> None:
        await self.claude.close()
        await self.gpt.close()
        await self.mistral.close()
        await self.granite.close()
