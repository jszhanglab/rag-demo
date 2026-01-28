"use client";
import { useEffect, useState } from "react";
import UploadArea from "./UploadArea";
import PDFViewer from "./PDFViewer";

type ViewerProps = {
  docId: string | null;
  //page: number;
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
          ></UploadArea>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full bg-white">
      <PDFViewer key={docId} docId={docId} />
    </div>
  );
}
