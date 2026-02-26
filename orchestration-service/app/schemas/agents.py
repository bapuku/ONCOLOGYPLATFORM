"""Agent-related schemas."""
from pydantic import BaseModel
from typing import List, Optional, Any


class TaskDecomposition(BaseModel):
    task_id: str
    agent: str
    description: str
    priority: int
    dependencies: List[str] = []


class OrchestrationPlan(BaseModel):
    workflow_id: str
    goal: str
    tasks: List[TaskDecomposition]
    estimated_duration_seconds: int


class AgentExecuteRequest(BaseModel):
    task_description: str
    patient_id: Optional[str] = None
    context: Optional[dict[str, Any]] = None
