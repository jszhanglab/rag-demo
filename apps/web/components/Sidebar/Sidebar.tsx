"use client";

import { API_ROUTES } from "@/constants/apiRoutes";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { useRouter, useSearchParams, usePathname } from "next/navigation"; // 引入路由 Hook
import useSWR from "swr";

const fetcher = (url: string) =>
  fetch(url)
    .then((r) => r.json())
    .then((res) => res.document_list);

export default function Sidebar() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  // 从当前 URL 中读取选中的 doc ID
  const selectedFileId = searchParams.get("doc");

  const { data, isLoading, error } = useSWR(API_ROUTES.GET_FILE_LIST, fetcher, {
    revalidateOnFocus: false,
  });

  const [hoveredFile, setHoveredFile] = useState<string | null>(null);
  const [showOptions, setShowOptions] = useState<string | null>(null);
  const [showDialog, setShowDialog] = useState<string | null>(null);
  const [fileHandleMode, setFileHandleMode] = useState<"rename" | "delete">(
    "rename",
  );

  const i18n = useTranslations("sidebar");

  if (isLoading) return <div className="p-4">{i18n("loading")}</div>;
  if (error) return <div className="p-4 text-red-600">{i18n("fail")}</div>;

  const handleFileClick = (fileId: string) => {
    const params = new URLSearchParams(searchParams.toString());

    if (selectedFileId === fileId) {
      params.delete("doc");
    } else {
      params.set("doc", fileId);
    }

    router.push(`${pathname}?${params.toString()}`);
  };

  const toggleOptions = (e: React.MouseEvent, fileId: string) => {
    e.stopPropagation();
    setShowOptions(showOptions === fileId ? null : fileId);
  };

  return (
    <div className="p-4 text-sm space-y-2">
      <ul className="space-y-1">
        {data?.map((doc: any) => (
          <li
            key={doc.id}
            className={`
              group relative flex items-center justify-between rounded-lg px-2 py-2 
              hover:bg-slate-200/60 cursor-pointer transition-all
              ${selectedFileId === doc.id ? "bg-white shadow-sm ring-1 ring-slate-200 text-blue-600 font-medium" : "text-slate-600"}
              h-9
            `}
            onClick={() => handleFileClick(doc.id)}
            onMouseEnter={() => setHoveredFile(doc.id)}
            onMouseLeave={() => setHoveredFile(null)}
          >
            <span className="truncate flex-1">{doc.filename}</span>

            {/* 更多选项按钮（三个点） */}
            {(hoveredFile === doc.id || showOptions === doc.id) && (
              <div
                className="flex items-center justify-center w-6 h-6 rounded-md hover:bg-slate-300 transition-colors"
                onClick={(e) => toggleOptions(e, doc.id)}
              >
                <span className="text-lg mb-2 font-bold text-slate-500">
                  ...
                </span>
              </div>
            )}

            {/* 操作菜单 */}
            {showOptions === doc.id && (
              <>
                <div
                  className="fixed inset-0 z-40"
                  onClick={() => setShowOptions(null)}
                />
                <div className="absolute top-full right-0 mt-1 p-1 bg-white border border-slate-200 shadow-xl rounded-lg w-32 z-50">
                  <button
                    className="block w-full px-3 py-1.5 text-left text-slate-700 hover:bg-slate-100 rounded-md transition-colors"
                    onClick={(e) => {
                      e.stopPropagation();
                      setFileHandleMode("rename");
                      setShowDialog(doc.id);
                      setShowOptions(null);
                    }}
                  >
                    {i18n("rename_btn")}
                  </button>
                  <button
                    className="block w-full px-3 py-1.5 text-left text-red-500 hover:bg-red-50 rounded-md transition-colors"
                    onClick={(e) => {
                      e.stopPropagation();
                      setFileHandleMode("delete");
                      setShowDialog(doc.id);
                      setShowOptions(null);
                    }}
                  >
                    {i18n("delete_btn")}
                  </button>
                </div>
              </>
            )}

            {/* 对话框 */}
            {showDialog === doc.id && (
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

// 简单的对话框实现
function FileOptionDialog({
  mode,
  fileId,
  onClose,
}: {
  mode: string;
  fileId: string;
  onClose: () => void;
}) {
  const i18n = useTranslations("sidebar");
  return (
    <>
      <div
        className="fixed inset-0 bg-slate-900/20 backdrop-blur-[2px] z-[100]"
        onClick={onClose}
      />
      <div className="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white shadow-2xl rounded-2xl w-80 p-6 z-[101]">
        <h3 className="text-lg font-bold mb-4">
          {mode === "rename" ? i18n("rename_btn") : i18n("delete_btn")}
        </h3>
        <div className="flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-3 py-1.5 text-sm font-medium text-slate-600 hover:bg-slate-100 rounded-md"
          >
            {i18n("dialog_cancel_btn")}
          </button>
          <button className="px-3 py-1.5 text-sm font-medium text-white bg-blue-600 rounded-md">
            {i18n("dialog_ok_btn")}
          </button>
        </div>
      </div>
    </>
  );
}
