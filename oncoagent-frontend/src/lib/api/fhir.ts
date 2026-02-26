import { API_BASE } from "@/lib/constants";
import { api } from "./client";

export async function getFhirResource(
  type: string,
  id: string
): Promise<unknown> {
  return api.get(`${API_BASE}/api/v1/fhir/${type}/${id}`);
}
