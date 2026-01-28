"use client";

import { useRouter, useSearchParams } from "next/navigation";
import Sidebar from "@/components/Sidebar/Sidebar";
import Viewer from "@/components/Viewer/Viewer";
import ChatPanel from "@/components/ChatPanel/ChatPanel";

export default function WorkspaceClient() {
  const router = useRouter();
  const sp = useSearchParams();

  const docId = sp.get("doc");

  const onSelectDocId = (newDocId: string) => {
    const params = new URLSearchParams(sp.toString());
    params.set("doc", newDocId);
    params.set("page", "1");
    router.replace(`?${params.toString()}`);
  };

  return (
    <>
      <section className="overflow-y-auto bg-slate-50">
        <Sidebar />
      </section>

      <section className="overflow-y-auto bg-white">
        <Viewer docId={docId} onSelectDocId={onSelectDocId} />
      </section>

      <section className="overflow-y-auto bg-white">
        <ChatPanel docId={docId} />
      </section>
    </>
  );
}
