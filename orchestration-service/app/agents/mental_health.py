"""Mental health support agent per spec §3 MentalHealthSupportAgent."""
from typing import Any, Optional
import json
from app.agents.base import BaseAgent
from app.schemas.responses import AgentResponse

MENTAL_HEALTH_SYSTEM_PROMPT = """You are the MentalHealthSupportAgent, a compassionate counselor AI within an integrated oncology platform.

CORE DIRECTIVES:
1. Detect emotional distress in patient communications using validated screening tools (PHQ-9, GAD-7).
2. Provide empathetic, evidence-based psychological support appropriate for cancer patients.
3. Assess distress level on a 0-10 scale. For distress_score >= 4: recommend professional support. For >= 7: notify care team via OrchestrationAgent.
4. Never replace professional mental health care - always recommend human therapist for clinical concerns.
5. Provide coping strategies, mindfulness exercises, and resource referrals.
6. Maintain cultural sensitivity and adapt communication style to patient preferences.

SAFETY GUARDRAILS:
- If suicidal ideation detected: immediate escalation to crisis team + emergency contact
- Always validate emotions before providing suggestions
- Never minimize patient's experience
- Document all interactions for continuity of care

OUTPUT FORMAT:
Return valid JSON with: agent_id, situation_summary, supporting_evidence, confidence, human_oversight_required, json_metrics (distress_score, phq9_estimate, escalation_needed, interventions_suggested), vocal_summary."""


class MentalHealthSupportAgent(BaseAgent):
    AGENT_ID = "MentalHealthSupportAgent"
    BACKBONE_MODEL = "claude_sonnet_4"
    SYSTEM_PROMPT = MENTAL_HEALTH_SYSTEM_PROMPT

    async def execute(
        self,
        task_description: str,
        patient_id: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> AgentResponse:
        prompt = f"""Assess the following patient communication for emotional well-being.
MESSAGE/TASK: {task_description}
PATIENT_ID: {patient_id or 'unknown'}
CONTEXT: {json.dumps(context or {})}

Assess distress level, provide empathetic response, and recommend interventions.
Return JSON with: agent_id, situation_summary, supporting_evidence, confidence, human_oversight_required, json_metrics (distress_score, escalation_needed, interventions_suggested), vocal_summary."""

        content = await self._call_llm(prompt, response_format="json")
        try:
            data = json.loads(content)
            return AgentResponse(
                agent_id=self.AGENT_ID,
                situation_summary=data.get("situation_summary", content[:200]),
                supporting_evidence=data.get("supporting_evidence"),
                confidence=float(data.get("confidence", 0.0)),
                human_oversight_required=data.get("human_oversight_required", True),
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
