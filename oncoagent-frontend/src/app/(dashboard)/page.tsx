import Link from "next/link";

export default function DashboardPage() {
  return (
    <div>
      <h1 className="text-2xl font-bold">Dashboard</h1>
      <p className="text-muted-foreground mt-2">
        Welcome to the OncoAgent Platform. Use the sidebar to navigate.
      </p>
      <div className="mt-6 flex gap-4">
        <Link href="/ai-assistant" className="text-primary hover:underline">
          Open AI Assistant
        </Link>
        <Link href="/patients" className="text-primary hover:underline">
          Patients
        </Link>
      </div>
    </div>
  );
}
