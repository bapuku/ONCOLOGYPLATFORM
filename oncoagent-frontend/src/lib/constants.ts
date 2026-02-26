/** OncoAgent Platform - API base URL */
export const API_BASE =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const API_AI = `${API_BASE}/api/v1/ai`;
export const API_AGENTS = `${API_BASE}/api/v1/agents`;
export const API_WORKFLOWS = `${API_BASE}/api/v1/workflows`;
