"""RBAC + ABAC middleware per spec §compliance.security.access_control."""
from typing import Any
from fastapi import Request, HTTPException
import structlog

logger = structlog.get_logger()

# Role definitions per spec
ROLES = {
    "oncologist": {"patient_access": True, "ai_interaction": True, "feedback": True},
    "radiologist": {"imaging_access": True, "imaging_agent": True},
    "nurse": {"patient_communication": True, "alerts": True, "symptom_tracking": True},
    "researcher": {"anonymized_data": True, "aggregate_analytics": True},
    "patient": {"own_data": True, "chatbot": True, "symptom_tracking": True},
    "admin": {"system_config": True, "user_management": True},
}


def get_user_role(request: Request) -> str:
    """Extract user role from request. Stub: returns 'oncologist' for development."""
    # Production: extract from JWT/SSO token
    return request.headers.get("X-User-Role", "oncologist")


def require_role(*allowed_roles: str):
    """Dependency that checks user has an allowed role."""
    async def check(request: Request) -> str:
        role = get_user_role(request)
        if role not in allowed_roles:
            logger.warning("access_denied", role=role, allowed=allowed_roles, path=request.url.path)
            raise HTTPException(status_code=403, detail=f"Role '{role}' not permitted for this resource")
        return role
    return check
