"""FHIR R4 proxy and ingestion - stub. Connect to FHIR server for live data."""
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/{resource_type}/{resource_id}")
async def get_fhir_resource(resource_type: str, resource_id: str) -> dict:
    """Fetch a FHIR resource. Stub: returns placeholder until FHIR server is configured."""
    allowed = (
        "Patient",
        "Condition",
        "Observation",
        "DiagnosticReport",
        "MedicationRequest",
        "Procedure",
        "CarePlan",
        "Encounter",
        "ServiceRequest",
    )
    if resource_type not in allowed:
        raise HTTPException(status_code=400, detail=f"Unknown resource type: {resource_type}")
    return {
        "resourceType": resource_type,
        "id": resource_id,
        "meta": {"versionId": "1"},
        "status": "stub",
        "message": "Configure FHIR server URL for live data",
    }
