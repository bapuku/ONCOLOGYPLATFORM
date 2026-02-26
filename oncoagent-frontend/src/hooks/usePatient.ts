"use client";

import { useState, useEffect } from "react";
import { getPatient } from "@/lib/api/patients";
import type { Patient } from "@/lib/types/patient";

export function usePatient(patientId: string | null) {
  const [patient, setPatient] = useState<Patient | null>(null);
  const [loading, setLoading] = useState(!!patientId);
  useEffect(() => {
    if (!patientId) {
      setPatient(null);
      setLoading(false);
      return;
    }
    setLoading(true);
    getPatient(patientId).then((p) => {
      setPatient(p ?? null);
      setLoading(false);
    });
  }, [patientId]);
  return { patient, loading };
}
