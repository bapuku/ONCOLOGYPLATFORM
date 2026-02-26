"""Medical literature research agent per spec §3 LiteratureAgent."""
from typing import Any, Optional
import json
from app.agents.base import BaseAgent
from app.schemas.responses import AgentResponse

LITERATURE_SYSTEM_PROMPT = """You are the LiteratureAgent, an oncology research expert within an integrated oncology AI platform.

CORE DIRECTIVES:
1. Search and analyze medical literature relevant to patient queries, treatment decisions, or research questions.
2. Prioritize evidence by level: meta-analyses > RCTs > cohort studies > case series > expert opinion.
3. Always cite sources with PubMed IDs, DOIs, or guideline references (ESMO, NCCN, ASCO).
4. Summarize key findings in situation_summary, list citations in supporting_evidence.
5. Assess the strength and applicability of evidence to the specific clinical context.
6. Write vocal_summary in patient-friendly language.

DATA SOURCES:
- PubMed/MEDLINE, Cochrane Library
- ESMO Clinical Practice Guidelines
- NCCN Guidelines
- ClinicalTrials.gov
- FDA/EMA drug labels

OUTPUT FORMAT:
Always return valid JSON with: agent_id, situation_summary, supporting_evidence, confidence, human_oversight_required, json_metrics (with source_count, evidence_level, guideline_references), vocal_summary."""


class LiteratureAgent(BaseAgent):
    AGENT_ID = "LiteratureAgent"
    BACKBONE_MODEL = "claude_sonnet_4"
    SYSTEM_PROMPT = LITERATURE_SYSTEM_PROMPT

    async def execute(
        self,
        task_description: str,
        patient_id: Optional[str] = None,
        context: Optional[dict[str, Any]] = None,
    ) -> AgentResponse:
        prompt = f"""Research the following clinical question using available oncology literature.
QUESTION: {task_description}
PATIENT_ID: {patient_id or 'unknown'}
CONTEXT: {json.dumps(context or {})}

Return a JSON response with: agent_id, situation_summary, supporting_evidence (with citations), confidence (0-1), human_oversight_required, json_metrics (source_count, evidence_level, guideline_references), vocal_summary."""

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
