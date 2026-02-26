"""Palliative care integration agent per spec §3 PalliativeCareAgent."""
from typing import Any, Optional
import json
from app.agents.base import BaseAgent
from app.schemas.responses import AgentResponse

PALLIATIVE_SYSTEM_PROMPT = """You are the PalliativeCareAgent, integrating palliative care into the oncology treatment pathway.

CORE DIRECTIVES:
1. Identify patients who would benefit from palliative care integration (symptom burden, prognosis, goals of care).
2. Assess symptom burden using validated tools (ESAS, PPS, ECOG).
3. Recommend symptom management strategies with evidence grading.
4. Facilitate advance care planning discussions and document preferences.
5. Coordinate with MentalHealthSupportAgent for psychosocial aspects.
6. Ensure holistic approach: physical, emotional, spiritual, social dimensions.

TRIGGERS FOR ACTIVATION:
- Pain score > 4/10 persistent for > 48h
- Multiple uncontrolled symptoms
- Prognosis discussion needed
- Treatment transition points (curative to palliative intent)
- Patient/family request

OUTPUT FORMAT:
Return valid JSON with: agent_id, situation_summary, supporting_evidence, confidence, human_oversight_required (true), json_metrics (symptom_scores, palliative_needs_score, recommendations), vocal_summary."""


class PalliativeCareAgent(BaseAgent):
    AGENT_ID = "PalliativeCareAgent"
    BACKBONE_MODEL = "claude_sonnet_4"
    SYSTEM_PROMPT = PALLIATIVE_SYSTEM_PROMPT

    async def execute(
        self,
        task_description: str,
        patient_id: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> AgentResponse:
        prompt = f"""Assess palliative care needs for the following.
TASK: {task_description}
PATIENT_ID: {patient_id or 'unknown'}
CONTEXT: {json.dumps(context or {})}

Assess symptom burden, palliative care integration needs, and recommend interventions.
Return JSON with: agent_id, situation_summary, supporting_evidence, confidence, human_oversight_required, json_metrics (symptom_scores, palliative_needs_score, recommendations), vocal_summary."""

        content = await self._call_llm(prompt, response_format="json")
        try:
            data = json.loads(content)
            return AgentResponse(
                agent_id=self.AGENT_ID,
                situation_summary=data.get("situation_summary", content[:200]),
                supporting_evidence=data.get("supporting_evidence"),
                confidence=float(data.get("confidence", 0.0)),
                human_oversight_required=True,
                json_metrics=data.get("json_metrics"),
                vocal_summary=data.get("vocal_summary"),
            )
        except (json.JSONDecodeError, ValueError):
            return AgentResponse(
                agent_id=self.AGENT_ID,
                situation_summary=content[:500],
                confidence=0.0,
                human_oversight_required=True,
            )
