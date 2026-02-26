import { API_BASE } from "@/lib/constants";
import { api } from "./client";
import type { Patient } from "@/lib/types/patient";

export async function getPatients(): Promise<Patient[]> {
  return api.get<Patient[]>(`${API_BASE}/api/v1/patients`).catch(() => []);
}

export async function getPatient(id: string): Promise<Patient | null> {
  return api.get<Patient>(`${API_BASE}/api/v1/patients/${id}`).catch(() => null);
}
