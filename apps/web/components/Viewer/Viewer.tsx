"use client";
import { useEffect, useState } from "react";

type ViewerProps = {
  docId: string | null;
  page: number;
};

export default function Viewer({ docId, page }: ViewerProps) {
  const [html, setHtml] = useState<string>("");

  useEffect(() => {
    if (!docId) {
      setHtml(
        "<div class='p-8 text-muted-foreground'>No document selected.</div>"
      );
      return;
    }

    // Mock preview
    setHtml(
      `<div style="padding:24px">Preview of <b>${docId}</b> — page ${page}</div>`
    );
  }, [docId, page]);

  return (
    <div className="min-h-full">
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </div>
  );
}
