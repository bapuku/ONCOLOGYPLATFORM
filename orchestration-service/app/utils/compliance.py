"""Compliance and audit utilities per spec §compliance (EU AI Act, GDPR)."""
from typing import Any
from datetime import datetime, timezone
import json
import structlog

logger = structlog.get_logger()

# In-memory audit log for development; production uses immutable store per spec
_audit_log: list[dict[str, Any]] = []


def audit_log(
    action: str,
    resource: str,
    user_id: str = "system",
    agent_id: str | None = None,
    details: dict[str, Any] | None = None,
    confidence: float | None = None,
    model_version: str | None = None,
) -> None:
    """Log an auditable action per EU AI Act Article 12 record-keeping requirements.

    Log content per spec:
    - Timestamp, User ID (pseudonymized), Query/Input, AI Output,
      Confidence scores, Model version, Reasoning trace,
      Human oversight action, Data sources accessed.
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "resource": resource,
        "user_id": user_id,
        "agent_id": agent_id,
        "confidence": confidence,
        "model_version": model_version,
        "details": details or {},
    }
    _audit_log.append(entry)
    logger.info("audit", **entry)


def get_audit_log(limit: int = 100) -> list[dict[str, Any]]:
    """Return recent audit entries (most recent first)."""
    return list(reversed(_audit_log[-limit:]))


def check_consent(patient_id: str, purpose: str = "ai_care_support") -> bool:
    """Check patient consent per GDPR consent management.
    Stub: returns True; production checks FHIR Consent resource.
    """
    logger.info("consent_check", patient_id=patient_id, purpose=purpose, result="granted_stub")
    return True


def pseudonymize(patient_id: str) -> str:
    """Pseudonymize patient ID for analytics/logs per GDPR privacy_by_design."""
    import hashlib
    return hashlib.sha256(f"oncoagent:{patient_id}".encode()).hexdigest()[:16]
