"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface TimelineEvent {
  id: string;
  date: string;
  type: "diagnosis" | "treatment" | "imaging" | "lab" | "note";
  title: string;
  description: string;
}

interface PatientTimelineProps {
  events?: TimelineEvent[];
  className?: string;
}

const TYPE_COLORS: Record<string, string> = {
  diagnosis: "bg-red-500",
  treatment: "bg-blue-500",
  imaging: "bg-purple-500",
  lab: "bg-green-500",
  note: "bg-yellow-500",
};

export function PatientTimeline({ events = [], className }: PatientTimelineProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="text-base">Patient Timeline</CardTitle>
      </CardHeader>
      <CardContent>
        {events.length === 0 ? (
          <p className="text-sm text-muted-foreground">
            No timeline events. Connect FHIR for live data.
          </p>
        ) : (
          <div className="relative border-l-2 border-muted pl-6 space-y-4">
            {events.map((event) => (
              <div key={event.id} className="relative">
                <div
                  className={`absolute -left-[31px] top-1 w-3 h-3 rounded-full ${TYPE_COLORS[event.type] || "bg-muted"}`}
                />
                <p className="text-xs text-muted-foreground">{event.date}</p>
                <p className="font-medium text-sm">{event.title}</p>
                <p className="text-sm text-muted-foreground">{event.description}</p>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
