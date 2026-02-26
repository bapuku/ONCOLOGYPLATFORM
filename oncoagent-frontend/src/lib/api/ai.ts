import { API_AI, API_AGENTS } from "@/lib/constants";
import { api } from "./client";
import type { AgentResponse } from "@/lib/types/ai";

export interface ChatRequest {
  message: string;
  patient_id?: string;
  context?: Record<string, unknown>;
}

export interface ChatResponse {
  content: string;
  agent_id?: string;
  confidence?: number;
  human_oversight_required?: boolean;
}

export async function sendChat(body: ChatRequest): Promise<ChatResponse> {
  return api.post<ChatResponse>(`${API_AI}/chat`, body);
}

export async function executeAgent(
  task_description: string,
  patient_id?: string,
  context?: Record<string, unknown>
): Promise<AgentResponse> {
  return api.post<AgentResponse>(`${API_AGENTS}/execute`, {
    task_description,
    patient_id,
    context,
  });
}
