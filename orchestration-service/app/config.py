"""Application configuration - OncoAgent Orchestration Service."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Settings loaded from environment."""

    app_name: str = "OncoAgent Orchestration Service"
    app_version: str = "1.0.0"

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""

    # Weaviate
    weaviate_url: str = "http://localhost:8080"

    # CORS
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    # LLM providers
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    mistral_api_key: str = ""
    granite_endpoint: str = "http://localhost:8001/v1/chat/completions"

    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"

    @property
    def NEO4J_URI(self) -> str:
        return self.neo4j_uri

    @property
    def NEO4J_USER(self) -> str:
        return self.neo4j_user

    @property
    def NEO4J_PASSWORD(self) -> str:
        return self.neo4j_password

    @property
    def WEAVIATE_URL(self) -> str:
        return self.weaviate_url

    @property
    def ALLOWED_ORIGINS(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
