"use client";
import Link from "next/link";

export default function Header() {
  return (
    <header className="h-[var(--header-h)] flex items-center justify-between px-4 border-b bg-background">
      <div className="font-semibold">🧠 RAG Demo (Mock)</div>
      <nav className="flex gap-2 text-sm">
        <Link href="/zh" className="hover:underline">
          中文
        </Link>
        <Link href="/en" className="hover:underline">
          EN
        </Link>
        <Link href="/ja" className="hover:underline">
          日本語
        </Link>
      </nav>
    </header>
  );
}
