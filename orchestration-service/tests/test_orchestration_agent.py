"""Tests for OrchestrationAgent - per spec §11."""
import pytest
from app.agents.orchestrator import OrchestrationAgent
from app.schemas.agents import OrchestrationPlan
from app.schemas.responses import AgentResponse


@pytest.mark.asyncio
async def test_plan_workflow_creates_valid_plan(orchestration_agent):
    plan = await orchestration_agent.plan_workflow(
        goal="Create treatment plan for patient",
        patient_id="patient-123",
    )
    assert isinstance(plan, OrchestrationPlan)
    assert plan.workflow_id == "test-1"
    assert plan.goal == "test"


@pytest.mark.asyncio
async def test_execute_workflow_returns_agent_response(orchestration_agent):
    plan = OrchestrationPlan(
        workflow_id="test-1",
        goal="Test goal",
        tasks=[],
        estimated_duration_seconds=60,
    )
    result = await orchestration_agent.execute_workflow(
        plan, patient_id="patient-123"
    )
    assert isinstance(result, AgentResponse)
    assert result.agent_id == "OrchestrationAgent"


@pytest.mark.asyncio
async def test_human_oversight_required_for_treatment_decisions(orchestration_agent):
    """EU AI Act compliance: human oversight required for treatment decisions."""
    plan = await orchestration_agent.plan_workflow(
        goal="Recommend new treatment for patient",
        patient_id="patient-123",
    )
    result = await orchestration_agent.execute_workflow(plan)
    assert result.human_oversight_required is True
