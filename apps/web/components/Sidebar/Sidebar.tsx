// apps/web/components/Sidebar/Sidebar.tsx
"use client";

import { API_ROUTES } from "@/constants/apiRoutes";
import { useTranslations } from "next-intl";
import { useState } from "react";
import useSWR from "swr";

const fetcher = (url: string) =>
  fetch(url)
    .then((r) => r.json())
    .then((res) => res.document_list);

export default function Sidebar() {
  const { data, isLoading, error } = useSWR(API_ROUTES.GET_FILE_LIST, fetcher, {
    revalidateOnFocus: false, //Prevent auto refetch on re-focus in layout(e.g. refocus on browser)
  });

  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [hoveredFile, setHoveredFile] = useState<string | null>(null); // Track hovered file
  const [showOptions, setShowOptions] = useState<string | null>(null);
  const [showDialog, setShowDialog] = useState<string | null>(null);
  const [fileHandleMode, setFileHandleMode] = useState<"rename" | "delete">(
    "rename"
  );
  const i18n = useTranslations("sidebar");

  if (isLoading) return <div className="p-4">{i18n("loading")}</div>;

  if (error) return <div className="p-4 text-red-600">{i18n("fail")}</div>;

  const handleFileClick = (fileId: string) => {
    setSelectedFile(fileId === selectedFile ? null : fileId); // Toggle selection
  };

  const toggleOptions = (e: React.MouseEvent, fileId: string) => {
    e.stopPropagation();
    setShowOptions(showOptions === fileId ? null : fileId); // Toggle options visibility
  };

  return (
    <div className="p-4 text-sm space-y-2">
      <ul className="space-y-1">
        {data?.map((doc: any) => (
          <li
            key={doc.id}
            className={`
              group relative flex items-center justify-between rounded-lg px-2 py-2 
              hover:bg-slate-100 cursor-pointer transition-all
              ${selectedFile === doc.id ? "bg-blue-100" : ""}
              h-8
            `}
            onClick={() => handleFileClick(doc.id)}
            onMouseEnter={() => setHoveredFile(doc.id)} // Mouse enter to show options
            onMouseLeave={() => setHoveredFile(null)} // Mouse leave to hide options
          >
            <span
              className={`truncate flex-1 ${
                selectedFile === doc.id ? "pr-6" : "group-hover:pr-6"
              }`}
            >
              {doc.filename}
            </span>

            {hoveredFile === doc.id && (
              <div
                className="flex items-center justify-center w-6 h-6 rounded-md hover:bg-black/10 transition-colors"
                onClick={(e) => toggleOptions(e, doc.id)}
              >
                <span className="text-xl leading-none">&#8942;</span>
              </div>
            )}

            {showOptions === doc.id && (
              <>
                <div
                  className="fixed inset-0 z-40"
                  onClick={(e) => {
                    e.stopPropagation();
                    setShowOptions(null);
                  }}
                />

                <div className="absolute top-10 right-0 p-1 bg-white/80 backdrop-blur-md border border-slate-200 shadow-xl rounded-xl w-32 z-50 animate-in fade-in zoom-in duration-150">
                  <button
                    className="block w-full px-3 py-1.5 text-left text-slate-700 hover:bg-blue-500 hover:text-white rounded-lg transition-colors"
                    onClick={() => {
                      setShowDialog("rename");
                      setShowOptions(null);
                      setFileHandleMode("rename");
                    }}
                  >
                    {i18n("rename_btn")}
                  </button>
                  <button
                    className="block w-full px-3 py-1.5 text-left text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                    onClick={() => {
                      setShowDialog("delete");
                      setShowOptions(null);
                      setFileHandleMode("delete");
                    }}
                  >
                    {i18n("delete_btn")}
                  </button>
                </div>
              </>
            )}
            {showDialog && (
              <FileOptionDialog
                mode={fileHandleMode}
                fileId={doc.id}
                onClose={() => setShowDialog(null)}
              />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}

//TODO Dialog

interface FileOptionDialogProps {
  mode: "rename" | "delete";
  fileId: string;
  onClose: () => void;
}

function FileOptionDialog({ mode, fileId, onClose }: FileOptionDialogProps) {
  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/[0.15] z-40"
        onClick={() => {
          onClose();
        }}
      ></div>

      {/* Modal */}
      <div className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none">
        <div className="bg-white shadow-xl rounded-xl w-120 p-12">
          <h3 className="text-xl font-semibold mb-4">File Options</h3>

          <div className="space-y-4">
            <button
              className="w-full p-2 text-left text-gray-700 hover:bg-blue-100 rounded-md"
              onClick={() => {
                // Handle rename logic
                console.log("Rename clicked");
                onClose();
              }}
            >
              Rename
            </button>
            <button
              className="w-full p-2 text-left text-red-500 hover:bg-red-100 rounded-md"
              onClick={() => {
                // Handle delete logic
                console.log("Delete clicked");
                onClose();
              }}
            >
              Delete
            </button>
          </div>

          {/* Close button */}
          <button
            className="absolute top-2 right-2 text-xl text-gray-600"
            onClick={onClose}
          >
            &times;
          </button>
        </div>
      </div>
    </>
  );
}
