"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const nav = [
  { href: "/", label: "Dashboard" },
  { href: "/patients", label: "Patients" },
  { href: "/ai-assistant", label: "AI Assistant" },
  { href: "/tumor-board", label: "Tumor Board" },
  { href: "/workflows", label: "Workflows" },
  { href: "/settings", label: "Settings" },
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="w-56 border-r bg-muted/30 flex flex-col">
      <div className="p-4 font-semibold border-b">OncoAgent</div>
      <nav className="p-2 flex-1">
        {nav.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "block px-3 py-2 rounded-md text-sm",
              pathname === item.href
                ? "bg-primary text-primary-foreground"
                : "hover:bg-muted"
            )}
          >
            {item.label}
          </Link>
        ))}
      </nav>
    </aside>
  );
}
