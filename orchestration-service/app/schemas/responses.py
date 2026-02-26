"""Standard response schemas."""
from pydantic import BaseModel
from typing import Optional, Any


class AgentResponse(BaseModel):
    """Standard agent output format per platform spec."""
    agent_id: str
    situation_summary: str
    supporting_evidence: Optional[str] = None
    confidence: float = 0.0
    human_oversight_required: bool = False
    json_metrics: Optional[dict[str, Any]] = None
    vocal_summary: Optional[str] = None
