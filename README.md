# OncoAgent Platform (HIPPOCRATES)

Oncology Agentic AI Platform — development, integration, and deployment per `oncology-platform-spec.yml`.

## Structure

- **oncology-platform-spec.yml** — Single source of truth (model registry, architecture, agents, deployment, compliance).
- **orchestration-service/** — FastAPI backend: multi-agent orchestration, LLM router, GraphRAG/Neo4j/Weaviate stubs, FHIR proxy.
- **oncoagent-frontend/** — Next.js 15 frontend: dashboard, AI Assistant (AIChatInterface), patients, workflows, settings.
- **deployment/** — Terraform stub, Helm chart, Prometheus config for CI/CD and observability.

## Quick start

### Backend

```bash
cd orchestration-service
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # edit if needed
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd oncoagent-frontend
npm install
npm run dev
```

Set `NEXT_PUBLIC_API_URL=http://localhost:8000` if the API is not on the same host.

### Tests

- Backend: `cd orchestration-service && pytest tests/ -v`
- Frontend: `cd oncoagent-frontend && npm run test`

## Compliance

Per spec: EU AI Act (high-risk), GDPR, human oversight on all treatment recommendations, confidence scores and audit trail. See `oncology-platform-spec.yml` sections `compliance` and `global_formatting`.
