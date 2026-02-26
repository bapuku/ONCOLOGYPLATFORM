"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface RiskScore {
  label: string;
  score: number;
  maxScore: number;
  level: "low" | "moderate" | "high";
}

interface RiskScoreDisplayProps {
  scores?: RiskScore[];
  className?: string;
}

const LEVEL_COLORS: Record<string, string> = {
  low: "bg-green-500",
  moderate: "bg-yellow-500",
  high: "bg-red-500",
};

export function RiskScoreDisplay({ scores = [], className }: RiskScoreDisplayProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-base">Risk Scores</CardTitle>
      </CardHeader>
      <CardContent>
        {scores.length === 0 ? (
          <p className="text-sm text-muted-foreground">No risk scores computed.</p>
        ) : (
          <div className="space-y-3">
            {scores.map((s) => (
              <div key={s.label}>
                <div className="flex justify-between text-sm mb-1">
                  <span>{s.label}</span>
                  <span className="font-medium">
                    {s.score}/{s.maxScore}
                  </span>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${LEVEL_COLORS[s.level]}`}
                    style={{ width: `${(s.score / s.maxScore) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
