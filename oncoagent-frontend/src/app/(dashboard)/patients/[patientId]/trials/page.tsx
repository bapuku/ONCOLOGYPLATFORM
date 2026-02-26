"use client";

import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";

export default function TrialsPage() {
  const { patientId } = useParams<{ patientId: string }>();

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Clinical Trials - Patient {patientId}</h1>
        <Badge variant="outline">TrialMatchingAgent</Badge>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Matched Trials</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="border rounded p-3">
              <div className="flex items-center justify-between mb-1">
                <span className="font-medium text-sm">No trials matched yet</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Use the AI Assistant to trigger TrialMatchingAgent for this patient.
                Matches are based on diagnosis, biomarkers, treatment history, and
                performance status.
              </p>
            </div>
          </div>
          <p className="mt-3 text-xs text-muted-foreground">
            Sources: ClinicalTrials.gov, EU Clinical Trials Register, institutional DB.
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Eligibility Criteria</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Select a matched trial above to view inclusion/exclusion criteria
            with per-criterion patient match status.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
