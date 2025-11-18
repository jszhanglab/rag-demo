"use client";
import { useEffect, useState } from "react";
import UploadArea from "./UploadArea";

type ViewerProps = {
  docId: string | null;
  page: number;
};

export default function Viewer({ docId, page }: ViewerProps) {
  const [html, setHtml] = useState<string>("");

  useEffect(() => {
    if (!docId) {
      setHtml("");
      return;
    }

    // Mock 预览内容
    setHtml(
      `<div style="padding:24px">Preview of <b>${docId}</b> — page ${page}</div>`
    );
  }, [docId, page]);

  if (!docId) {
    return (
      <div className="h-full bg-white flex items-center justify-center">
        <div className="text-sm text-slate-500">
          <UploadArea></UploadArea>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-white">
      <div className="h-full p-6">
        <div
          className="text-sm text-slate-800"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      </div>
    </div>
  );
}
