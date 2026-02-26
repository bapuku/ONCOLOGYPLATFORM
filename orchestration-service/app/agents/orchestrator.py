"""Orchestration agent - plans and executes multi-agent workflows."""
from typing import Dict, List, Optional, Any
from app.agents.base import BaseAgent
from app.schemas.responses import AgentResponse
from app.schemas.agents import TaskDecomposition, OrchestrationPlan
from app.models.llm_router import LLMRouter
from app.rag.graph_rag import GraphRAGEngine
from app.rag.context_builder import ContextBuilder
from app.knowledge.ontology_validator import OntologyValidator
import structlog

logger = structlog.get_logger()


class OrchestrationAgent(BaseAgent):
    """Central orchestration agent. Coordinates all other agents."""

    AGENT_ID = "OrchestrationAgent"
    BACKBONE_MODEL = "claude_opus_4"

    def __init__(
        self,
        llm_router: LLMRouter,
        graph_rag: GraphRAGEngine,
        context_builder: ContextBuilder,
        ontology_validator: OntologyValidator,
    ):
        self.llm_router = llm_router
        self.graph_rag = graph_rag
        self.context_builder = context_builder
        self.ontology_validator = ontology_validator
        self._agent_registry: Dict[str, BaseAgent] = {}

    def register_agent(self, agent: BaseAgent) -> None:
        self._agent_registry[agent.AGENT_ID] = agent
        logger.info("Registered agent", agent_id=agent.AGENT_ID)

    async def plan_workflow(
        self,
        goal: str,
        patient_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> OrchestrationPlan:
        kg_context = await self.context_builder.build_patient_context(patient_id) if patient_id else {}
        planning_prompt = f"""
You are the OrchestrationAgent for an oncology AI platform.
GOAL: {goal}
PATIENT CONTEXT: {kg_context}
ADDITIONAL CONTEXT: {context}
AVAILABLE AGENTS: {list(self._agent_registry.keys())}
Decompose this goal into specific tasks. Return JSON with workflow_id, goal, tasks (task_id, agent, description, priority, dependencies), estimated_duration_seconds.
"""
        response = await self.llm_router.generate(
            prompt=planning_prompt,
            model_id=self.BACKBONE_MODEL,
            response_format="json",
        )
        try:
            return OrchestrationPlan.model_validate_json(response.content)
        except Exception:
            import uuid
            return OrchestrationPlan(
                workflow_id=str(uuid.uuid4())[:8],
                goal=goal,
                tasks=[],
                estimated_duration_seconds=0,
            )

    async def execute_workflow(
        self,
        plan: OrchestrationPlan,
        patient_id: Optional[str] = None,
    ) -> AgentResponse:
        results: Dict[str, AgentResponse] = {}
        completed_tasks: set = set()
        pending_tasks = list(plan.tasks)
        pending_tasks.sort(key=lambda t: t.priority)

        while pending_tasks:
            ready = [t for t in pending_tasks if all(d in completed_tasks for d in t.dependencies)]
            if not ready:
                break
            for task in ready:
                agent = self._agent_registry.get(task.agent)
                if not agent:
                    continue
                dep_ctx = {d: results[d].json_metrics for d in task.dependencies if d in results} if results else {}
                result = await agent.execute(
                    task_description=task.description,
                    patient_id=patient_id,
                    context=dep_ctx,
                )
                results[task.task_id] = result
                completed_tasks.add(task.task_id)
                pending_tasks.remove(task)
        return await self._synthesize_results(plan, results)

    async def _synthesize_results(
        self,
        plan: OrchestrationPlan,
        results: Dict[str, AgentResponse],
    ) -> AgentResponse:
        if not results:
            return AgentResponse(
                agent_id=self.AGENT_ID,
                situation_summary=f"Processed goal: {plan.goal}. Configure LLM API keys for full multi-agent orchestration.",
                confidence=0.0,
                human_oversight_required=True,
            )
        text = "\n".join(
            f"=== {r.agent_id} (Task: {tid}) ===\nSummary: {r.situation_summary}\nEvidence: {r.supporting_evidence}\nConfidence: {r.confidence}\nHuman Oversight: {r.human_oversight_required}"
            for tid, r in results.items()
        )
        prompt = f"Synthesize into cohesive care plan. GOAL: {plan.goal}\nAGENT RESULTS:\n{text}\nReturn JSON with: agent_id, situation_summary, supporting_evidence, json_metrics, vocal_summary, human_oversight_required, confidence."
        response = await self.llm_router.generate(
            prompt=prompt,
            model_id=self.BACKBONE_MODEL,
            response_format="json",
        )
        try:
            return AgentResponse.model_validate_json(response.content)
        except Exception:
            return AgentResponse(
                agent_id=self.AGENT_ID,
                situation_summary=response.content[:500],
                confidence=0.0,
                human_oversight_required=True,
            )

    async def execute(
        self,
        task_description: str,
        patient_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> AgentResponse:
        plan = await self.plan_workflow(task_description, patient_id=patient_id, context=context)
        return await self.execute_workflow(plan, patient_id=patient_id)
