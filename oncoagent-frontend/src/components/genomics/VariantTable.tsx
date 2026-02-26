"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

interface Variant {
  gene: string;
  variant: string;
  classification: string;
  actionability: "high" | "medium" | "low" | "unknown";
  evidence: string;
}

interface VariantTableProps {
  variants?: Variant[];
  className?: string;
}

const ACTIONABILITY_COLORS: Record<string, "default" | "secondary" | "outline" | "destructive"> = {
  high: "default",
  medium: "secondary",
  low: "outline",
  unknown: "outline",
};

export function VariantTable({ variants = [], className }: VariantTableProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-base">Genomic Variants</CardTitle>
      </CardHeader>
      <CardContent>
        {variants.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            No variants loaded. Upload VCF or connect FHIR Genomics.
          </p>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-left text-muted-foreground">
                  <th className="p-2">Gene</th>
                  <th className="p-2">Variant</th>
                  <th className="p-2">Classification</th>
                  <th className="p-2">Actionability</th>
                  <th className="p-2">Evidence</th>
                </tr>
              </thead>
              <tbody>
                {variants.map((v, i) => (
                  <tr key={i} className="border-b">
                    <td className="p-2 font-medium">{v.gene}</td>
                    <td className="p-2">{v.variant}</td>
                    <td className="p-2">{v.classification}</td>
                    <td className="p-2">
                      <Badge variant={ACTIONABILITY_COLORS[v.actionability]}>
                        {v.actionability}
                      </Badge>
                    </td>
                    <td className="p-2">{v.evidence}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <p className="mt-2 text-xs text-muted-foreground">
          Sources: ClinVar, COSMIC, OncoKB
        </p>
      </CardContent>
    </Card>
  );
}
