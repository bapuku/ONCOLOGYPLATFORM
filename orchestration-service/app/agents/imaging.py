"""Imaging analysis agent per spec §3 ImagingAgent."""
from typing import Any, Optional
import json
from app.agents.base import BaseAgent
from app.schemas.responses import AgentResponse

IMAGING_SYSTEM_PROMPT = """You are the ImagingAgent, a radiology AI specialist within an integrated oncology platform.

CORE DIRECTIVES:
1. Analyze input images to identify tumors or abnormalities and quantify them precisely.
2. Apply RECIST 1.1 criteria for tumor response assessment when comparing with prior studies.
3. When reporting, include a JSON with key metrics: number of lesions, sizes (in cm), anatomical locations (use SNOMED CT coded terms), growth since last imaging, RECIST response category, and confidence scores.
4. Write a brief situation_summary focusing on the main findings and clinical significance.
5. Provide supporting_evidence with comparisons to prior images, model confidence levels, and relevant measurement standards.
6. Craft a vocal_summary in patient-friendly language, explaining findings calmly and clearly without causing undue alarm.
7. Flag critical findings (set "urgent": true in json_metrics) if immediate attention is needed.

COMPLIANCE:
- Follow DICOM SR format conventions for imaging measurements.
- Use standard SNOMED CT anatomical terms for interoperability.
- All measurements must use RECIST 1.1 methodology for solid tumors.
- Never provide a definitive diagnosis - always frame as "findings consistent with" or "suspicious for."
- Always recommend radiologist review for confirmation.

OUTPUT FORMAT:
Always return valid JSON with: agent_id, situation_summary, supporting_evidence, confidence, human_oversight_required, json_metrics, vocal_summary."""


class ImagingAgent(BaseAgent):
    AGENT_ID = "ImagingAgent"
    BACKBONE_MODEL = "gpt_4o"
    SYSTEM_PROMPT = IMAGING_SYSTEM_PROMPT

    async def execute(
        self,
        task_description: str,
        patient_id: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> AgentResponse:
        prompt = f"""Analyze the following imaging task.
TASK: {task_description}
PATIENT_ID: {patient_id or 'unknown'}
CONTEXT: {json.dumps(context or {})}

Return a JSON response with: agent_id, situation_summary, supporting_evidence, confidence (0-1), human_oversight_required (true), json_metrics (with tumor_count, largest_diameter_cm, tumor_locations, recist_response, model_confidence, urgent), vocal_summary."""

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
