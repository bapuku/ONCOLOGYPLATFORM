"use client";

import { useState, useCallback } from "react";
import { sendChat } from "@/lib/api/ai";
import type { AIMessage } from "@/lib/types/ai";

interface UseAIChatOptions {
  patientId?: string;
  context?: "general" | "patient" | "tumor_board";
}

export function useAIChat({ patientId, context = "general" }: UseAIChatOptions = {}) {
  const [messages, setMessages] = useState<AIMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentAgent, setCurrentAgent] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim()) return;
      const userMessage: AIMessage = {
        id: `user-${Date.now()}`,
        role: "user",
        content,
      };
      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setCurrentAgent(null);
      try {
        const res = await sendChat({
          message: content,
          patient_id: patientId,
          context: { context },
        });
        const assistantMessage: AIMessage = {
          id: `ai-${Date.now()}`,
          role: "assistant",
          content: res.content,
          agentId: res.agent_id,
          confidence: res.confidence,
          humanOversightRequired: res.human_oversight_required,
          structuredResponse: res.content
            ? {
                situation_summary: res.content,
                confidence: res.confidence,
                human_oversight_required: res.human_oversight_required,
              }
            : undefined,
        };
        setMessages((prev) => [...prev, assistantMessage]);
        setCurrentAgent(res.agent_id ?? null);
      } catch (err) {
        const errorMessage: AIMessage = {
          id: `ai-${Date.now()}`,
          role: "assistant",
          content: err instanceof Error ? err.message : "Request failed",
        };
        setMessages((prev) => [...prev, errorMessage]);
      } finally {
        setIsLoading(false);
      }
    },
    [patientId, context]
  );

  return { messages, isLoading, sendMessage, currentAgent };
}
