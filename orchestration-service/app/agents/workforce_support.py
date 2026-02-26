"""Workforce training and wellness agent per spec §3 WorkforceSupportAgent."""
from typing import Any, Optional
import json
from app.agents.base import BaseAgent
from app.schemas.responses import AgentResponse

WORKFORCE_SYSTEM_PROMPT = """You are the WorkforceSupportAgent, supporting the oncology care team's professional development and well-being.

CORE DIRECTIVES:
1. Provide personalized training recommendations based on role and experience level.
2. Detect burnout indicators from workload patterns and communication analysis.
3. Suggest evidence-based wellness interventions.
4. Generate workload distribution reports and identify imbalances.
5. Facilitate peer support connections and mentorship matching.
6. Track continuing education requirements and certifications.

OUTPUT FORMAT:
Return valid JSON with: agent_id, situation_summary, supporting_evidence, confidence, human_oversight_required, json_metrics (burnout_risk_score, training_recommendations, workload_metrics), vocal_summary."""


class WorkforceSupportAgent(BaseAgent):
    AGENT_ID = "WorkforceSupportAgent"
    BACKBONE_MODEL = "claude_sonnet_4"
    SYSTEM_PROMPT = WORKFORCE_SYSTEM_PROMPT

    async def execute(
        self,
        task_description: str,
        patient_id: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> AgentResponse:
        prompt = f"""Assess workforce support needs.
TASK: {task_description}
CONTEXT: {json.dumps(context or {})}

Return JSON with: agent_id, situation_summary, supporting_evidence, confidence, human_oversight_required, json_metrics, vocal_summary."""

        content = await self._call_llm(prompt, response_format="json")
        try:
            data = json.loads(content)
            return AgentResponse(
                agent_id=self.AGENT_ID,
                situation_summary=data.get("situation_summary", content[:200]),
                supporting_evidence=data.get("supporting_evidence"),
                confidence=float(data.get("confidence", 0.0)),
                human_oversight_required=data.get("human_oversight_required", False),
                json_metrics=data.get("json_metrics"),
                vocal_summary=data.get("vocal_summary"),
            )
        except (json.JSONDecodeError, ValueError):
            return AgentResponse(
                agent_id=self.AGENT_ID,
                situation_summary=content[:500],
                confidence=0.0,
                human_oversight_required=False,
            )
