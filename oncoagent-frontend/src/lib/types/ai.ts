export interface AIMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  agentId?: string;
  confidence?: number;
  humanOversightRequired?: boolean;
  structuredResponse?: {
    situation_summary?: string;
    supporting_evidence?: string | string[];
    confidence?: number;
    human_oversight_required?: boolean;
    json_metrics?: Record<string, unknown>;
    vocal_summary?: string;
  };
}

export interface AgentResponse {
  agent_id: string;
  situation_summary: string;
  supporting_evidence?: string | null;
  confidence: number;
  human_oversight_required: boolean;
  json_metrics?: Record<string, unknown> | null;
  vocal_summary?: string | null;
}
