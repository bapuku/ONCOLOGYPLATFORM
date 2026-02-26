"""AI chat and orchestration API."""
from fastapi import APIRouter, Request
from app.schemas.ai import ChatRequest, ChatResponse
from app.schemas.responses import AgentResponse
from app.utils.compliance import audit_log, check_consent, pseudonymize

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: Request, body: ChatRequest) -> ChatResponse:
    """Handle chat message; delegate to orchestration agent."""
    app = request.app
    orchestrator = getattr(app.state, "orchestrator", None)
    if not orchestrator:
        return ChatResponse(
            content="Orchestration service not initialized.",
            human_oversight_required=True,
        )

    if body.patient_id:
        check_consent(body.patient_id)

    result: AgentResponse = await orchestrator.execute(
        task_description=body.message,
        patient_id=body.patient_id,
        context=body.context,
    )

    audit_log(
        action="ai_chat",
        resource=f"patient/{pseudonymize(body.patient_id or 'general')}",
        agent_id=result.agent_id,
        confidence=result.confidence,
        details={"query_length": len(body.message), "human_oversight": result.human_oversight_required},
    )

    return ChatResponse(
        content=result.situation_summary or result.vocal_summary or "",
        agent_id=result.agent_id,
        confidence=result.confidence,
        human_oversight_required=result.human_oversight_required,
    )


@router.get("/audit")
async def get_audit(limit: int = 50) -> dict:
    """Return recent audit log entries per EU AI Act Article 12."""
    from app.utils.compliance import get_audit_log
    return {"entries": get_audit_log(limit)}
