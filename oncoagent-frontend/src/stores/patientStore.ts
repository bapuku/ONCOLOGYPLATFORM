import { create } from "zustand";
import type { Patient } from "@/lib/types/patient";

interface PatientState {
  selected: Patient | null;
  setSelected: (p: Patient | null) => void;
}

export const usePatientStore = create<PatientState>((set) => ({
  selected: null,
  setSelected: (p) => set({ selected: p }),
}));
