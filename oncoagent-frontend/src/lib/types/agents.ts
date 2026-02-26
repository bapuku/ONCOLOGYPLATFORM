export const AGENT_IDS = [
  "OrchestrationAgent",
  "ImagingAgent",
  "LiteratureAgent",
  "TrialMatchingAgent",
  "EthicsGuardianAgent",
  "MentalHealthSupportAgent",
  "PalliativeCareAgent",
  "WorkforceSupportAgent",
] as const;

export type AgentId = (typeof AGENT_IDS)[number];
