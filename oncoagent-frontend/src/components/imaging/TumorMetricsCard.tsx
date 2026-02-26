"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface TumorMetrics {
  tumorCount?: number;
  largestDiameterCm?: number;
  recistResponse?: string;
  modelConfidence?: number;
  urgent?: boolean;
}

interface TumorMetricsCardProps {
  metrics?: TumorMetrics;
  className?: string;
}

export function TumorMetricsCard({ metrics, className }: TumorMetricsCardProps) {
  const m = metrics || {};
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-base flex items-center justify-between">
          Tumor Metrics (RECIST 1.1)
          {m.urgent && <Badge variant="destructive">Urgent</Badge>}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-2 text-sm">
          <Row label="Lesion Count" value={m.tumorCount?.toString()} />
          <Row label="Largest Diameter" value={m.largestDiameterCm ? `${m.largestDiameterCm} cm` : undefined} />
          <Row label="RECIST Response" value={m.recistResponse} />
          <Row label="AI Confidence" value={m.modelConfidence ? `${Math.round(m.modelConfidence * 100)}%` : undefined} />
        </div>
      </CardContent>
    </Card>
  );
}

function Row({ label, value }: { label: string; value?: string }) {
  return (
    <div className="flex justify-between">
      <span className="text-muted-foreground">{label}</span>
      <span className="font-medium">{value || "--"}</span>
    </div>
  );
}
