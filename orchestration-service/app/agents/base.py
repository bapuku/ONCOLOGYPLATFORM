"""Base agent and standard response type per spec §3."""
from abc import ABC, abstractmethod
from typing import Any, Optional
import structlog
from app.schemas.responses import AgentResponse
from app.models.llm_router import LLMRouter

logger = structlog.get_logger()


class BaseAgent(ABC):
    """Base class for all platform agents."""

    AGENT_ID: str = "BaseAgent"
    BACKBONE_MODEL: str = "claude_sonnet_4"
    SYSTEM_PROMPT: str = ""

    def __init__(self, llm_router: LLMRouter | None = None) -> None:
        self.llm_router = llm_router

    async def _call_llm(
        self,
        prompt: str,
        system: str | None = None,
        response_format: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Call LLM via router. Returns raw content string."""
        if not self.llm_router:
            return '{"agent_id":"' + self.AGENT_ID + '","situation_summary":"No LLM router configured.","confidence":0.0,"human_oversight_required":true}'
        resp = await self.llm_router.generate(
            prompt=prompt,
            model_id=self.BACKBONE_MODEL,
            system=system or self.SYSTEM_PROMPT,
            response_format=response_format,
            **kwargs,
        )
        return resp.content

    @abstractmethod
    async def execute(
        self,
        task_description: str,
        patient_id: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> AgentResponse:
        """Execute a task and return standardized AgentResponse."""
        ...

    async def _safe_execute(
        self,
        task_description: str,
        patient_id: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> AgentResponse:
        """Wrap execute with error handling."""
        try:
            return await self.execute(task_description, patient_id, context)
        except Exception as e:
            logger.error("Agent execution failed", agent=self.AGENT_ID, error=str(e))
            return AgentResponse(
                agent_id=self.AGENT_ID,
                situation_summary=f"Agent error: {str(e)}",
                confidence=0.0,
                human_oversight_required=True,
            )
