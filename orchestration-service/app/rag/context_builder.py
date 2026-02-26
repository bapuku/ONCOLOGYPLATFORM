"""Build patient context from knowledge graph - spec §2-3."""
from typing import Any
from app.knowledge.neo4j_client import Neo4jClient
import structlog

logger = structlog.get_logger()


class ContextBuilder:
    """Builds context for agents from KG. Uses Neo4j when available."""

    def __init__(self, neo4j_client: Neo4jClient | None = None) -> None:
        self.neo4j = neo4j_client

    async def build_patient_context(self, patient_id: str | None) -> dict[str, Any]:
        """Build patient summary from knowledge graph for orchestration context."""
        if not patient_id:
            return {}
        if not self.neo4j:
            return {"patient_id": patient_id, "summary": "No KG connected."}
        try:
            cypher = (
                "MATCH (p:Patient {id: $id})-[:HAS*0..2]-(n) "
                "RETURN p, collect(n) as nodes LIMIT 1"
            )
            rows = await self.neo4j.query(cypher, {"id": patient_id})
            if not rows:
                return {"patient_id": patient_id, "summary": "No patient data in KG."}
            return {"patient_id": patient_id, "kg_data": rows[0]}
        except Exception as e:
            logger.warning("build_patient_context failed", error=str(e))
            return {"patient_id": patient_id, "error": str(e)}
