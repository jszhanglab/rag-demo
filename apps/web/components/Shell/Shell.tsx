/**
 * Layout（服务器端框架）
 *   └── Shell（客户端交互框架）
 *         └── Page（页面内容）
 */
"use client";

import { useState } from "react";

export default function Shell({ children }: { children: React.ReactNode }) {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <>
      {/* Replace with your real Header if you already have one */}
      <header className="h-[var(--header-h)] border-b px-4 flex items-center justify-between">
        <div className="font-semibold">RAG Demo</div>
        <button
          className="text-sm border px-2 py-1 rounded"
          onClick={() => setSidebarOpen((v) => !v)}
        >
          {sidebarOpen ? "Hide sidebar" : "Show sidebar"}
        </button>
      </header>

      <main
        className={[
          "min-h-[calc(100vh-var(--header-h))] grid",
          sidebarOpen
            ? "grid-cols-[18rem_1fr_28rem]" // Sidebar | Viewer | Chat
            : "grid-cols-[0px_1fr_28rem]", // Collapse sidebar to 0
        ].join(" ")}
      >
        {children}
      </main>
    </>
  );
}
