"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface TrialMatch {
  nctId: string;
  title: string;
  phase: string;
  eligibilityScore: number;
  status: string;
}

interface TrialMatchCardProps {
  trial: TrialMatch;
  className?: string;
}

export function TrialMatchCard({ trial, className }: TrialMatchCardProps) {
  const scorePct = Math.round(trial.eligibilityScore * 100);
  return (
    <Card className={className}>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <CardTitle className="text-sm">{trial.nctId}</CardTitle>
          <Badge variant={scorePct >= 80 ? "default" : "secondary"}>
            {scorePct}% match
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-sm font-medium">{trial.title}</p>
        <div className="flex gap-2 mt-2 text-xs text-muted-foreground">
          <span>Phase {trial.phase}</span>
          <span>|</span>
          <span>{trial.status}</span>
        </div>
      </CardContent>
    </Card>
  );
}
