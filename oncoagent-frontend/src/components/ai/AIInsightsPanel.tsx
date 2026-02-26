"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface Insight {
  id: string;
  title: string;
  summary: string;
  agentId?: string;
  confidence?: number;
}

interface AIInsightsPanelProps {
  insights?: Insight[];
  className?: string;
}

export function AIInsightsPanel({ insights = [], className }: AIInsightsPanelProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-base">AI Insights</CardTitle>
      </CardHeader>
      <CardContent>
        {insights.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            No insights yet. Use the AI assistant to generate insights.
          </p>
        ) : (
          <ul className="space-y-3">
            {insights.map((i) => (
              <li key={i.id} className="text-sm border-l-2 pl-3">
                <p className="font-medium">{i.title}</p>
                <p className="text-muted-foreground">{i.summary}</p>
                {i.agentId && (
                  <span className="text-xs text-muted-foreground">
                    Source: {i.agentId}
                  </span>
                )}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
