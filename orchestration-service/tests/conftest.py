"""Pytest configuration and fixtures."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from app.agents.orchestrator import OrchestrationAgent
from app.rag.graph_rag import GraphRAGResult


@pytest.fixture
def mock_llm_router():
    router = MagicMock()
    async def generate(prompt, **kwargs):
        if "Synthesize" in prompt or "human_oversight" in (prompt or "").lower():
            return MagicMock(
                content='{"agent_id":"OrchestrationAgent","situation_summary":"Test synthesis","supporting_evidence":null,"confidence":0.9,"human_oversight_required":true,"json_metrics":null,"vocal_summary":null}'
            )
        return MagicMock(
            content='{"workflow_id": "test-1", "goal": "test", "tasks": [], "estimated_duration_seconds": 60}'
        )
    router.generate = AsyncMock(side_effect=generate)
    return router


@pytest.fixture
def mock_graph_rag():
    rag = MagicMock()
    rag.retrieve = AsyncMock(
        return_value=GraphRAGResult(
            graph_subgraph=[],
            vector_results=[],
            hyperedge_matches=[],
        )
    )
    return rag


@pytest.fixture
def mock_context_builder():
    cb = MagicMock()
    cb.build_patient_context = AsyncMock(return_value={})
    return cb


@pytest.fixture
def orchestration_agent(mock_llm_router, mock_graph_rag, mock_context_builder):
    return OrchestrationAgent(
        llm_router=mock_llm_router,
        graph_rag=mock_graph_rag,
        context_builder=mock_context_builder,
        ontology_validator=MagicMock(),
    )
