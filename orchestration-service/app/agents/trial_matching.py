"""Clinical trial matching agent per spec §3 TrialMatchingAgent."""
from typing import Any, Optional
import json
from app.agents.base import BaseAgent
from app.schemas.responses import AgentResponse

TRIAL_SYSTEM_PROMPT = """You are the TrialMatchingAgent, a clinical trial navigator within an integrated oncology AI platform.

CORE DIRECTIVES:
1. Match patients to eligible clinical trials based on their diagnosis, biomarkers, treatment history, and performance status.
2. Use structured eligibility criteria from ClinicalTrials.gov and institutional trial databases.
3. Score eligibility match percentage and explain inclusion/exclusion criteria met/unmet.
4. Prioritize phase III > phase II > phase I trials. Consider proximity and practical feasibility.
5. Provide situation_summary with top matched trials and rationale.

DATA SOURCES:
- ClinicalTrials.gov API
- EU Clinical Trials Register
- Institutional trial database
- ESMO/NCCN guideline-recommended trials

OUTPUT FORMAT:
Always return valid JSON with: agent_id, situation_summary, supporting_evidence, confidence, human_oversight_required (true), json_metrics (trial_matches: [{nct_id, title, phase, eligibility_score, key_criteria_met, key_criteria_unmet}]), vocal_summary."""


class TrialMatchingAgent(BaseAgent):
    AGENT_ID = "TrialMatchingAgent"
    BACKBONE_MODEL = "mistral_large"
    SYSTEM_PROMPT = TRIAL_SYSTEM_PROMPT

    async def execute(
        self,
        task_description: str,
        patient_id: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> AgentResponse:
        prompt = f"""Match the following patient to eligible clinical trials.
TASK: {task_description}
PATIENT_ID: {patient_id or 'unknown'}
CONTEXT: {json.dumps(context or {})}

Return a JSON response with: agent_id, situation_summary, supporting_evidence, confidence (0-1), human_oversight_required (true), json_metrics (with trial_matches array), vocal_summary."""

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
