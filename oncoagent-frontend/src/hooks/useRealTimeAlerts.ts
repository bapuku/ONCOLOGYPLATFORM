"use client";

import { useState, useEffect } from "react";

/** Placeholder for Socket.io real-time alerts per spec */
export function useRealTimeAlerts(_patientId?: string) {
  const [alerts, setAlerts] = useState<unknown[]>([]);
  useEffect(() => {
    // TODO: socket.io connection to backend for agent alerts
  }, [_patientId]);
  return { alerts };
}
