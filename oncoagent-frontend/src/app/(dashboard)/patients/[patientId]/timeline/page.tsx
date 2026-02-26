"use client";

import { useParams } from "next/navigation";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function TimelinePage() {
  const { patientId } = useParams<{ patientId: string }>();

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">Timeline - Patient {patientId}</h1>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Patient Timeline</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="relative border-l-2 border-muted pl-6 space-y-6">
            <TimelineEvent
              date="--"
              title="Diagnosis"
              description="Initial diagnosis and staging. Data from FHIR Condition."
              type="diagnosis"
            />
            <TimelineEvent
              date="--"
              title="Treatment Start"
              description="First treatment cycle. Data from FHIR MedicationRequest."
              type="treatment"
            />
            <TimelineEvent
              date="--"
              title="Imaging"
              description="Scan results with AI annotations. From ImagingAgent."
              type="imaging"
            />
            <TimelineEvent
              date="--"
              title="Lab Results"
              description="Key lab values with trend. From FHIR Observation."
              type="lab"
            />
          </div>
          <p className="mt-6 text-xs text-muted-foreground">
            Connect FHIR backend for live patient timeline with AI annotations.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

function TimelineEvent({
  date,
  title,
  description,
  type,
}: {
  date: string;
  title: string;
  description: string;
  type: string;
}) {
  const colors: Record<string, string> = {
    diagnosis: "bg-red-500",
    treatment: "bg-blue-500",
    imaging: "bg-purple-500",
    lab: "bg-green-500",
  };
  return (
    <div className="relative">
      <div
        className={`absolute -left-[31px] top-1 w-3 h-3 rounded-full ${colors[type] || "bg-muted"}`}
      />
      <p className="text-xs text-muted-foreground">{date}</p>
      <p className="font-medium text-sm">{title}</p>
      <p className="text-sm text-muted-foreground">{description}</p>
    </div>
  );
}
