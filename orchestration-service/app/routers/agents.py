"""Agents API - list and invoke agents."""
from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from app.schemas.agents import AgentExecuteRequest, OrchestrationPlan
from app.schemas.responses import AgentResponse

router = APIRouter()


class PlanWorkflowRequest(BaseModel):
    goal: str
    patient_id: Optional[str] = None


@router.get("/")
async def list_agents(request: Request) -> dict:
    """List registered agent IDs."""
    orchestrator = getattr(request.app.state, "orchestrator", None)
    if not orchestrator:
        return {"agents": []}
    return {"agents": list(orchestrator._agent_registry.keys())}


@router.post("/execute", response_model=AgentResponse)
async def execute_agent(request: Request, body: AgentExecuteRequest) -> AgentResponse:
    """Execute a task via orchestration (orchestrator delegates)."""
    orchestrator = getattr(request.app.state, "orchestrator", None)
    if not orchestrator:
        return AgentResponse(
            agent_id="system",
            situation_summary="Orchestration not available.",
            human_oversight_required=True,
        )
    return await orchestrator.execute(
        task_description=body.task_description,
        patient_id=body.patient_id,
        context=body.context,
    )


@router.post("/workflow/plan", response_model=OrchestrationPlan)
async def plan_workflow(request: Request, body: PlanWorkflowRequest) -> OrchestrationPlan:
    """Plan a workflow for a goal."""
    orchestrator = getattr(request.app.state, "orchestrator", None)
    if not orchestrator:
        return OrchestrationPlan(
            workflow_id="stub",
            goal=body.goal,
            tasks=[],
            estimated_duration_seconds=0,
        )
    return await orchestrator.plan_workflow(body.goal, patient_id=body.patient_id)
