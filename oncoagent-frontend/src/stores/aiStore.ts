import { create } from "zustand";

interface AIState {
  currentAgent: string | null;
  setCurrentAgent: (a: string | null) => void;
}

export const useAIStore = create<AIState>((set) => ({
  currentAgent: null,
  setCurrentAgent: (a) => set({ currentAgent: a }),
}));
