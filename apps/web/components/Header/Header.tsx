"use client";
import { useRouter, usePathname } from "next/navigation";
import { useTranslations } from "next-intl";

type HeaderProps = {
  locale: string;
  sidebarOpen: boolean;
  setSidebarOpen: (value: boolean) => void;
};

export default function Header({
  locale,
  sidebarOpen,
  setSidebarOpen,
}: HeaderProps) {
  const router = useRouter();
  const pathname = usePathname();
  const t = useTranslations("Header");

  const handleLocaleChange = (nextLocale: string) => {
    if (!pathname) {
      router.replace(`/${nextLocale}`);
      return;
    }

    const segments = pathname.split("/");
    if (segments.length > 1) {
      segments[1] = nextLocale;
      const newPath = segments.join("/") || "/";
      router.replace(newPath);
    } else {
      router.replace(`/${nextLocale}`);
    }
  };

  const sidebarTooltip = sidebarOpen
    ? t("sidebar.collapse")
    : t("sidebar.expand");

  return (
    <header className="h-[var(--header-h)] flex items-center justify-between px-4 border-b border-slate-200 bg-white">
      <div className="flex items-center gap-2">
        <div className="font-semibold text-sm">🧠 RAG Demo</div>

        <button
          onClick={() => setSidebarOpen(!sidebarOpen)}
          className="
            p-2 rounded-lg 
            bg-white 
            hover:bg-slate-100 
            transition-colors
          "
          aria-label={sidebarTooltip}
          title={sidebarTooltip}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.8"
            className="h-5 w-5 text-slate-600"
          >
            <rect x="5" y="5" width="16.5" height="16.5" rx="4" />
            <path d="M10.5 7v12.5" strokeLinecap="round" />
          </svg>
        </button>
      </div>

      <div className="flex items-center">
        <select
          className="text-sm border border-slate-300 rounded px-2 py-1 bg-white hover:bg-slate-50"
          value={locale}
          onChange={(e) => handleLocaleChange(e.target.value)}
        >
          <option value="en">English</option>
          <option value="zh">中文</option>
          <option value="ja">日本語</option>
        </select>
      </div>
    </header>
  );
}
