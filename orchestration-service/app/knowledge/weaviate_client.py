"""Weaviate vector store client per spec §2 architecture."""
from typing import Any
import structlog

logger = structlog.get_logger()


class WeaviateClient:
    """Weaviate client. Uses weaviate-client when available, falls back to stub."""

    def __init__(self, url: str) -> None:
        self.url = url
        self._client = None
        self._connected = False
        self._init_client()

    def _init_client(self) -> None:
        try:
            import weaviate
            self._client = weaviate.connect_to_local(
                host=self.url.replace("http://", "").split(":")[0],
                port=int(self.url.split(":")[-1]) if ":" in self.url.rsplit("/", 1)[-1] else 8080,
            )
            self._connected = True
            logger.info("Weaviate client connected", url=self.url)
        except ImportError:
            logger.warning("weaviate-client not installed; using stub mode")
        except Exception as e:
            logger.warning("Weaviate connection failed; using stub mode", error=str(e))

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def close(self) -> None:
        if self._client:
            self._client.close()
            self._client = None
            self._connected = False
        logger.info("Weaviate client closed")

    async def search(
        self,
        collection: str,
        query: str,
        top_k: int = 10,
        **kwargs: Any,
    ) -> list[dict[str, Any]]:
        """Vector search. Returns list of result dicts."""
        if not self._client:
            return []
        try:
            col = self._client.collections.get(collection)
            results = col.query.near_text(query=query, limit=top_k)
            return [{"properties": obj.properties, "score": getattr(obj.metadata, "distance", None)} for obj in results.objects]
        except Exception as e:
            logger.error("Weaviate search failed", error=str(e), collection=collection)
            return []

    async def ensure_schema(self) -> None:
        """Create Weaviate collections for oncology platform."""
        if not self._client:
            return
        collections = [
            {"name": "ClinicalDocument", "description": "Clinical notes and reports"},
            {"name": "PubMedArticle", "description": "PubMed literature for RAG"},
            {"name": "GuidelineChunk", "description": "ESMO/NCCN guideline chunks"},
            {"name": "PatientSummary", "description": "Patient context summaries"},
        ]
        for col in collections:
            try:
                if not self._client.collections.exists(col["name"]):
                    self._client.collections.create(name=col["name"])
                    logger.info("Created Weaviate collection", name=col["name"])
            except Exception as e:
                logger.warning("Weaviate schema creation failed", name=col["name"], error=str(e))
