"""OncoAgent Orchestration Service - HIPPOCRATES."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import structlog

from app.config import get_settings
from app.routers import ai, agents, workflows, fhir
from app.knowledge.neo4j_client import Neo4jClient
from app.knowledge.weaviate_client import WeaviateClient
from app.models.llm_router import LLMRouter
from app.rag.graph_rag import GraphRAGEngine
from app.rag.context_builder import ContextBuilder
from app.knowledge.ontology_validator import OntologyValidator
from app.agents.orchestrator import OrchestrationAgent
from app.agents.imaging import ImagingAgent
from app.agents.literature import LiteratureAgent
from app.agents.trial_matching import TrialMatchingAgent
from app.agents.ethics_guardian import EthicsGuardianAgent
from app.agents.mental_health import MentalHealthSupportAgent
from app.agents.palliative_care import PalliativeCareAgent
from app.agents.workforce_support import WorkforceSupportAgent

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logger.info("Starting OncoAgent Orchestration Service")
    app.state.neo4j = Neo4jClient(
        settings.NEO4J_URI, settings.NEO4J_USER, settings.NEO4J_PASSWORD
    )
    app.state.weaviate = WeaviateClient(settings.WEAVIATE_URL)
    llm_router = LLMRouter()
    app.state.llm_router = llm_router
    app.state.graph_rag = GraphRAGEngine(
        neo4j_client=app.state.neo4j,
        weaviate_client=app.state.weaviate,
    )
    app.state.context_builder = ContextBuilder(neo4j_client=app.state.neo4j)
    app.state.ontology_validator = OntologyValidator()

    orchestrator = OrchestrationAgent(
        llm_router=llm_router,
        graph_rag=app.state.graph_rag,
        context_builder=app.state.context_builder,
        ontology_validator=app.state.ontology_validator,
    )
    orchestrator.register_agent(ImagingAgent(llm_router=llm_router))
    orchestrator.register_agent(LiteratureAgent(llm_router=llm_router))
    orchestrator.register_agent(TrialMatchingAgent(llm_router=llm_router))
    orchestrator.register_agent(EthicsGuardianAgent(llm_router=llm_router))
    orchestrator.register_agent(MentalHealthSupportAgent(llm_router=llm_router))
    orchestrator.register_agent(PalliativeCareAgent(llm_router=llm_router))
    orchestrator.register_agent(WorkforceSupportAgent(llm_router=llm_router))
    app.state.orchestrator = orchestrator

    yield

    logger.info("Shutting down OncoAgent Orchestration Service")
    await llm_router.close()
    await app.state.neo4j.close()
    await app.state.weaviate.close()


app = FastAPI(
    title="OncoAgent Orchestration Service",
    description="Multi-agent orchestration for oncology AI platform",
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["Agents"])
app.include_router(workflows.router, prefix="/api/v1/workflows", tags=["Workflows"])
app.include_router(fhir.router, prefix="/api/v1/fhir", tags=["FHIR"])


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "services": {
            "neo4j": "connected",
            "weaviate": "connected",
            "llm_router": "ready",
        },
    }
