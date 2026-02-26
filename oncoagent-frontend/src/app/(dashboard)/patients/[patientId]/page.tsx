"use client";

import { useParams } from "next/navigation";
import { usePatient } from "@/hooks/usePatient";
import { AIChatInterface } from "@/components/ai/AIChatInterface";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";

export default function PatientDetailPage() {
  const { patientId } = useParams<{ patientId: string }>();
  const { patient, loading } = usePatient(patientId);

  if (loading) {
    return <p className="text-muted-foreground">Loading patient data...</p>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">
            {patient?.name || `Patient ${patientId}`}
          </h1>
          <p className="text-muted-foreground">
            MRN: {patient?.mrn || patientId} | DOB: {patient?.birthDate || "N/A"} |{" "}
            {patient?.gender || "N/A"}
          </p>
        </div>
        <Badge variant="outline">FHIR Connected</Badge>
      </div>

      <div className="flex gap-2 border-b pb-2 text-sm">
        <Link href={`/patients/${patientId}`} className="text-primary font-medium">
          Overview
        </Link>
        <Link href={`/patients/${patientId}/imaging`} className="hover:text-primary">
          Imaging
        </Link>
        <Link href={`/patients/${patientId}/genomics`} className="hover:text-primary">
          Genomics
        </Link>
        <Link href={`/patients/${patientId}/trials`} className="hover:text-primary">
          Trials
        </Link>
        <Link href={`/patients/${patientId}/timeline`} className="hover:text-primary">
          Timeline
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Clinical Summary</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Connect FHIR backend for live patient clinical data (Conditions,
                Observations, MedicationRequests, Procedures).
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Treatment Plan</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Treatment plan from OrchestrationAgent. Use AI Assistant to generate.
              </p>
            </CardContent>
          </Card>
        </div>

        <div className="h-[500px] border rounded-lg">
          <AIChatInterface patientId={patientId} context="patient" />
        </div>
      </div>
    </div>
  );
}
