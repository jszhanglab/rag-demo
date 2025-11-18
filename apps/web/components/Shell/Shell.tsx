/**
 * Layout
 *   └── Shell
 *       └── Header（i18n / UI）
 *       └── Page（Sidebar + Viewer + ChatPanel）
 */

"use client";

import { useState } from "react";
import "@/styles/layout.css";
import Header from "@/components/Header/Header";

export default function Shell({
  children,
  locale,
}: {
  children: React.ReactNode;
  locale: string;
}) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <div className="h-[var(--header-h)] border-b bg-white shadow-sm">
        <Header
          locale={locale}
          sidebarOpen={sidebarOpen}
          setSidebarOpen={setSidebarOpen}
        />
      </div>

      <main
        className={[
          "min-h-[calc(100vh-var(--header-h))] grid divide-x divide-slate-200",
          sidebarOpen
            ? "grid-cols-[18rem_1fr_26rem]" // Sidebar | Viewer | Chat
            : "grid-cols-[0px_1fr_26rem]",
        ].join(" ")}
      >
        {children}
      </main>
    </div>
  );
}
