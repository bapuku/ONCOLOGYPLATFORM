"use client";

import Link from "next/link";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { Patient } from "@/lib/types/patient";

interface PatientCardProps {
  patient: Patient;
}

export function PatientCard({ patient }: PatientCardProps) {
  return (
    <Link href={`/patients/${patient.id}`}>
      <Card className="hover:border-primary transition-colors cursor-pointer">
        <CardContent className="p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium">{patient.name}</p>
              <p className="text-sm text-muted-foreground">
                MRN: {patient.mrn || patient.id}
              </p>
            </div>
            <div className="text-right">
              <p className="text-sm text-muted-foreground">
                {patient.birthDate || "DOB N/A"}
              </p>
              <Badge variant="outline" className="text-xs">
                {patient.gender || "N/A"}
              </Badge>
            </div>
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
