"use client";

import { Card, CardContent } from "@/components/ui/card";

interface ReasoningTraceProps {
  steps?: string[];
  className?: string;
}

export function ReasoningTrace({ steps = [], className }: ReasoningTraceProps) {
  if (steps.length === 0) return null;
  return (
    <Card className={className}>
      <CardContent className="pt-4">
        <p className="text-xs font-medium text-muted-foreground mb-2">
          Reasoning trace
        </p>
        <ol className="list-decimal list-inside space-y-1 text-sm">
          {steps.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      </CardContent>
    </Card>
  );
}
