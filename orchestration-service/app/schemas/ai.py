"""AI request/response schemas."""
from pydantic import BaseModel
from typing import Optional, Any


class ChatRequest(BaseModel):
    """Incoming chat message."""
    message: str
    patient_id: Optional[str] = None
    context: Optional[dict[str, Any]] = None


class ChatResponse(BaseModel):
    """AI chat response."""
    content: str
    agent_id: Optional[str] = None
    confidence: Optional[float] = None
    human_oversight_required: bool = False
