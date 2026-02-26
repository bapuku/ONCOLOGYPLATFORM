"use client";

import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface ConfidenceBadgeProps {
  confidence: number;
  className?: string;
}

export function ConfidenceBadge({ confidence, className }: ConfidenceBadgeProps) {
  const pct = Math.round(confidence * 100);
  const variant = pct >= 80 ? "default" : pct >= 60 ? "secondary" : "outline";
  return (
    <Badge variant={variant} className={cn("text-xs", className)}>
      {pct}% confidence
    </Badge>
  );
}
