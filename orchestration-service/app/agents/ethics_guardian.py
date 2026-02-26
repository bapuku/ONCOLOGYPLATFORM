"""Ethics and compliance guardian agent per spec §3 EthicsGuardianAgent."""
from typing import Any, Optional
import json
from app.agents.base import BaseAgent
from app.schemas.responses import AgentResponse

ETHICS_SYSTEM_PROMPT = """You are the EthicsGuardianAgent, an ethical oversight AI within an integrated oncology platform.

CORE DIRECTIVES:
1. Continuously review communications from all other agents before they reach end users.
2. Check for: patient privacy violations, clinical safety issues, EU AI Act compliance, bias, and appropriate language.
3. Validate that all outputs include proper disclaimers, confidence scores, and human oversight flags.
4. Ensure no PII leaks in external API calls.
5. Monitor for demographic bias in recommendations.
6. Verify consent status before AI processing of patient data.

MONITORING RULES:
- Privacy: No patient identifiers in logs or external calls
- Clinical safety: Flag any recommendation without evidence citation
- EU AI Act: Verify transparency, human oversight, and documentation
- Bias: Check for demographic disparities in treatment recommendations
- Language: Ensure culturally sensitive, non-alarmist patient communications

OUTPUT FORMAT:
Return valid JSON with: agent_id, situation_summary (compliance status), supporting_evidence (rules checked), confidence, human_oversight_required, json_metrics (issues_found, rules_checked, compliance_score), vocal_summary."""


class EthicsGuardianAgent(BaseAgent):
    AGENT_ID = "EthicsGuardianAgent"
    BACKBONE_MODEL = "claude_4_5_sonnet"
    SYSTEM_PROMPT = ETHICS_SYSTEM_PROMPT

    async def execute(
        self,
        task_description: str,
        patient_id: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> AgentResponse:
        prompt = f"""Review the following for ethical and compliance issues.
CONTENT TO REVIEW: {task_description}
PATIENT_ID: {patient_id or 'N/A'}
CONTEXT: {json.dumps(context or {})}

Check privacy, clinical safety, EU AI Act compliance, bias, and language appropriateness.
Return JSON with: agent_id, situation_summary, supporting_evidence, confidence, human_oversight_required, json_metrics (issues_found, rules_checked, compliance_score), vocal_summary."""

        content = await self._call_llm(prompt, response_format="json")
        try:
            data = json.loads(content)
            return AgentResponse(
                agent_id=self.AGENT_ID,
                situation_summary=data.get("situation_summary", "Compliance check completed."),
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
