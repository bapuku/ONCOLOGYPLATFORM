"""Kafka producer/consumer for event-driven workflows - stub per spec §2 communication_orchestration."""
from typing import Any
import structlog

logger = structlog.get_logger()

# Topics from spec: events.agent.task_complete, events.agent.alert, etc.
AGENT_TOPICS = [
    "events.agent.task_complete",
    "events.agent.alert",
    "events.data.new_scan",
    "events.data.new_lab",
    "events.data.patient_message",
]


class KafkaClient:
    """Stub Kafka client. Configure bootstrap servers for production."""

    def __init__(self, bootstrap_servers: str = "localhost:9092") -> None:
        self.bootstrap_servers = bootstrap_servers

    async def publish(self, topic: str, key: str | None, value: dict[str, Any]) -> None:
        """Publish event. Stub: log only."""
        logger.info("kafka.publish", topic=topic, key=key, value=value)

    async def subscribe(self, topic: str, handler: Any) -> None:
        """Subscribe to topic. Stub: no-op until Kafka is configured."""
        logger.info("kafka.subscribe", topic=topic)
