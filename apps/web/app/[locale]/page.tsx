// apps/web/app/[locale]/page.tsx
import Sidebar from "@/components/Sidebar/Sidebar";
import Viewer from "@/components/Viewer/Viewer";
import ChatPanel from "@/components/ChatPanel/ChatPanel";

export default function Page({
  searchParams,
}: {
  searchParams?: { doc?: string; page?: string; thread?: string };
}) {
  const docId = searchParams?.doc ?? null;
  const page = Number(searchParams?.page ?? 1) || 1;
  const threadId = searchParams?.thread ?? null;

  // The 3 columns themselves are laid out by <main> in [locale]/layout.tsx.
  // We just render the three sections in order.
  return (
    <>
      {/* Left: Sidebar (your former DocsList) */}
      <section className="border-r overflow-y-auto">
        {/* You can pass selected docId if your Sidebar needs it later */}
        <Sidebar />
      </section>

      {/* Middle: Document viewer */}
      <section className="overflow-y-auto bg-white">
        <Viewer docId={docId} page={page} />
      </section>

      {/* Right: Chat panel */}
      <section className="border-l overflow-y-auto">
        <ChatPanel docId={docId} threadId={threadId} />
      </section>
    </>
  );
}
