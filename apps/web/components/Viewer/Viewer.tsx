"use client";
import { useEffect, useState } from "react";
import UploadArea from "./UploadArea";

import dynamic from "next/dynamic";

const PDFViewer = dynamic(() => import("./PDFViewer"), {
  ssr: false,
  loading: () => (
    <div className="h-full flex items-center justify-center bg-slate-50">
      <div className="flex flex-col items-center gap-2">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500" />
        <p className="text-xs text-slate-400">Loading PDF Engine...</p>
      </div>
    </div>
  ),
});

type ViewerProps = {
  docId: string | null;
  onSelectDocId: (docId: string) => void;
};

export default function Viewer({ docId, onSelectDocId }: ViewerProps) {
  if (!docId) {
    return (
      <div className="h-full bg-white flex justify-center">
        <div className="mt-24">
          <UploadArea
            onUploaded={(newDocId) => {
              onSelectDocId(newDocId);
            }}
          />
        </div>
      </div>
    );
  }

  return (
    <div className="h-full w-full relative overflow-hidden">
      <PDFViewer key={docId} docId={docId} />
    </div>
  );
}
