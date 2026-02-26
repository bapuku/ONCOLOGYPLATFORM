"use client";

import { useState } from "react";

/** Placeholder for workflow execution state */
export function useWorkflow() {
  const [running, setRunning] = useState(false);
  return { running, setRunning };
}
