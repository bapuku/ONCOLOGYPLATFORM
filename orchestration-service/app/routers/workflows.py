"""Workflows API - execute planned workflows."""
from fastapi import APIRouter, Request
from app.schemas.agents import OrchestrationPlan
from app.schemas.responses import AgentResponse

router = APIRouter()


@router.post("/execute", response_model=AgentResponse)
async def execute_workflow(
    request: Request,
    plan: OrchestrationPlan,
    patient_id: str | None = None,
) -> AgentResponse:
    """Execute a pre-computed orchestration plan."""
    orchestrator = getattr(request.app.state, "orchestrator", None)
    if not orchestrator:
        return AgentResponse(
            agent_id="system",
            situation_summary="Orchestration not available.",
            human_oversight_required=True,
        )
    return await orchestrator.execute_workflow(plan, patient_id=patient_id)
