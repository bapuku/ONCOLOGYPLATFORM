"use client";

import { useState, useRef, useEffect } from "react";
import { useAIChat } from "@/hooks/useAIChat";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Loader2, Send, Bot, User } from "lucide-react";
import { ReasoningTrace } from "./ReasoningTrace";
import { ConfidenceBadge } from "./ConfidenceBadge";
import type { AIMessage } from "@/lib/types/ai";

interface AIChatInterfaceProps {
  patientId?: string;
  context?: "general" | "patient" | "tumor_board";
}

export function AIChatInterface({
  patientId,
  context = "general",
}: AIChatInterfaceProps) {
  const [input, setInput] = useState("");
  const scrollRef = useRef<HTMLDivElement>(null);
  const { messages, isLoading, sendMessage, currentAgent } = useAIChat({
    patientId,
    context,
  });

  useEffect(() => {
    scrollRef.current?.scrollTo?.({ top: scrollRef.current.scrollHeight });
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    await sendMessage(input);
    setInput("");
  };

  const renderMessage = (message: AIMessage) => {
    const isUser = message.role === "user";
    return (
      <div
        key={message.id}
        className={`flex gap-3 ${isUser ? "justify-end" : "justify-start"}`}
      >
        {!isUser && (
          <div className="shrink-0 w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center">
            <Bot className="w-4 h-4 text-primary" />
          </div>
        )}
        <div className={`max-w-[80%] ${isUser ? "order-first" : ""}`}>
          {!isUser && message.agentId && (
            <div className="flex items-center gap-2 mb-1">
              <Badge variant="outline" className="text-xs">
                {message.agentId}
              </Badge>
              {message.confidence != null && (
                <ConfidenceBadge confidence={message.confidence} />
              )}
            </div>
          )}
          <Card
            className={isUser ? "bg-primary text-primary-foreground" : ""}
          >
            <CardContent className="p-3">
              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              {message.structuredResponse?.supporting_evidence && (
                <details className="text-xs mt-2">
                  <summary className="cursor-pointer font-medium">
                    Supporting Evidence
                  </summary>
                  <p className="mt-1 pl-2">
                    {Array.isArray(message.structuredResponse.supporting_evidence)
                      ? message.structuredResponse.supporting_evidence.join(", ")
                      : message.structuredResponse.supporting_evidence}
                  </p>
                </details>
              )}
            </CardContent>
          </Card>
        </div>
        {isUser && (
          <div className="shrink-0 w-8 h-8 rounded-full bg-muted flex items-center justify-center">
            <User className="w-4 h-4 text-muted-foreground" />
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-2 px-2 py-2 border-b">
        <span className="font-semibold">OncoAgent AI Assistant</span>
        {currentAgent && (
          <Badge variant="secondary">{currentAgent}</Badge>
        )}
      </div>
      <div ref={scrollRef} className="flex-1 overflow-auto p-4">
        <div className="space-y-4 min-h-[200px]">
          {messages.length === 0 && (
            <p className="text-sm text-muted-foreground text-center py-8">
              Send a message to start. Include patient context if needed.
            </p>
          )}
          {messages.map(renderMessage)}
          {isLoading && (
            <div className="flex gap-3 justify-start">
              <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center shrink-0">
                <Loader2 className="w-4 h-4 animate-spin text-primary" />
              </div>
              <Card>
                <CardContent className="p-3">
                  <p className="text-sm text-muted-foreground">
                    Analyzing with {currentAgent || "AI"}...
                  </p>
                </CardContent>
              </Card>
            </div>
          )}
        </div>
      </div>
      <form onSubmit={handleSubmit} className="p-4 border-t flex gap-2">
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about treatment, imaging, trials..."
          disabled={isLoading}
          className="flex-1"
        />
        <Button type="submit" disabled={isLoading || !input.trim()}>
          {isLoading ? (
            <Loader2 className="w-4 h-4 animate-spin" />
          ) : (
            <Send className="w-4 h-4" />
          )}
        </Button>
      </form>
    </div>
  );
}
