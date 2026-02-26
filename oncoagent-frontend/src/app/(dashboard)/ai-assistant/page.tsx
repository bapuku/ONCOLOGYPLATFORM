import { AIChatInterface } from "@/components/ai/AIChatInterface";
import { AIInsightsPanel } from "@/components/ai/AIInsightsPanel";

export default function AIAssistantPage() {
  return (
    <div className="h-[calc(100vh-8rem)] flex gap-4">
      <div className="flex-1 min-w-0">
        <AIChatInterface context="general" />
      </div>
      <div className="w-80 flex-shrink-0">
        <AIInsightsPanel />
      </div>
    </div>
  );
}
