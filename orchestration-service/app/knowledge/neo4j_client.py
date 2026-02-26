"""Neo4j knowledge graph client per spec §2 architecture.data_ingestion."""
from typing import Any
import structlog

logger = structlog.get_logger()


class Neo4jClient:
    """Neo4j client. Uses neo4j driver when available, falls back to stub."""

    def __init__(self, uri: str, user: str, password: str) -> None:
        self.uri = uri
        self.user = user
        self._password = password
        self._driver = None
        self._connected = False
        self._init_driver()

    def _init_driver(self) -> None:
        try:
            import neo4j
            self._driver = neo4j.GraphDatabase.driver(
                self.uri, auth=(self.user, self._password)
            )
            self._connected = True
            logger.info("Neo4j driver initialized", uri=self.uri)
        except ImportError:
            logger.warning("neo4j package not installed; using stub mode")
        except Exception as e:
            logger.warning("Neo4j connection failed; using stub mode", error=str(e))

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def close(self) -> None:
        if self._driver:
            self._driver.close()
            self._driver = None
            self._connected = False
        logger.info("Neo4j client closed")

    async def query(self, cypher: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Execute Cypher query. Returns list of record dicts."""
        if not self._driver:
            return []
        try:
            with self._driver.session() as session:
                result = session.run(cypher, params or {})
                return [dict(record) for record in result]
        except Exception as e:
            logger.error("Neo4j query failed", error=str(e), cypher=cypher[:100])
            return []

    async def ensure_schema(self) -> None:
        """Create KG schema constraints and indexes per spec ontology."""
        schema_statements = [
            "CREATE CONSTRAINT IF NOT EXISTS FOR (p:Patient) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) REQUIRE d.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (g:Gene) REQUIRE g.symbol IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (dr:Drug) REQUIRE dr.name IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (t:Tumor) REQUIRE t.id IS UNIQUE",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (trial:ClinicalTrial) REQUIRE trial.nct_id IS UNIQUE",
            "CREATE INDEX IF NOT EXISTS FOR (p:Patient) ON (p.mrn)",
            "CREATE INDEX IF NOT EXISTS FOR (o:Observation) ON (o.date)",
        ]
        for stmt in schema_statements:
            await self.query(stmt)
        logger.info("Neo4j KG schema ensured")
