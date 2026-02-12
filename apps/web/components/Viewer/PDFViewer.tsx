"use client";

import React, { useEffect, useRef } from "react";
import useSWR from "swr";
import { buildDocumentDetailUrl } from "@/constants/apiRouteBuilders";
import { useTranslations } from "next-intl";

import { Viewer, Worker } from "@react-pdf-viewer/core";
import { pageNavigationPlugin } from "@react-pdf-viewer/page-navigation";

import "@react-pdf-viewer/core/lib/styles/index.css";
import "@react-pdf-viewer/page-navigation/lib/styles/index.css";

type DocumentDetail = {
  id?: string;
  status: string;
  file_url?: string;
  ocr_text?: string | null;
};

interface PDFViewerProps {
  docId: string | null;
}

const fetcher = async (url: string): Promise<DocumentDetail> => {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${res.status}`);
  return res.json();
};

const PDFViewer: React.FC<PDFViewerProps> = ({ docId }) => {
  const t_viewer = useTranslations("viewer");

  const pageNavigationPluginInstance = pageNavigationPlugin();
  const { jumpToPage } = pageNavigationPluginInstance;
  const jumpToPageRef = useRef(jumpToPage);

  useEffect(() => {
    jumpToPageRef.current = jumpToPage;
  }, [jumpToPage]);

  const url = docId ? buildDocumentDetailUrl(docId) : null;

  // 优化轮询逻辑：只要是完成或失败状态，立即停止轮询 (0)
  const { data, error } = useSWR(url, fetcher, {
    refreshInterval: (latest) =>
      latest?.status === "EMBEDDING_DONE" || latest?.status === "FAILED"
        ? 0
        : 2000,
    revalidateOnFocus: false,
  });

  // 跳转监听逻辑
  useEffect(() => {
    const handleJump = (event: any) => {
      const { page } = event.detail;
      if (page && jumpToPageRef.current) {
        console.log(`[PDFViewer] 正在跳转至第 ${page} 页`);
        setTimeout(() => jumpToPageRef.current?.(page - 1), 300);
      }
    };
    window.addEventListener("jumpToPdfLocation", handleJump);
    return () => window.removeEventListener("jumpToPdfLocation", handleJump);
  }, []);

  if (!docId)
    return (
      <div className="h-full flex items-center justify-center bg-slate-50 text-slate-400 italic">
        请选择文档
      </div>
    );
  if (error)
    return (
      <div className="p-6 text-red-500 font-medium">
        加载失败: {error.message}
      </div>
    );

  const fileUrl = data?.file_url;
  const status = data?.status || "LOADING";

  return (
    <div className="h-full flex flex-col bg-slate-100 p-4 overflow-hidden">
      <div className="flex-1 flex flex-col bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden relative">
        {/* 顶部状态栏 */}
        <div className="px-6 py-3 border-b flex items-center justify-between bg-white z-10">
          <div className="flex items-center gap-2">
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">
              Document Viewer
            </span>
            <span
              className={`text-[10px] px-2 py-0.5 rounded-full border font-bold ${fileUrl ? "bg-emerald-50 text-emerald-600 border-emerald-100" : "bg-amber-50 text-amber-600 border-amber-100 animate-pulse"}`}
            >
              {status}
            </span>
          </div>
        </div>

        {/* PDF 内容区 */}
        <div className="flex-1 relative bg-slate-200">
          {fileUrl ? (
            <div className="absolute inset-0">
              <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js">
                <Viewer
                  fileUrl={fileUrl}
                  plugins={[pageNavigationPluginInstance]}
                  theme="light"
                />
              </Worker>
            </div>
          ) : (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-50">
              {status === "EMBEDDING_DONE" ? (
                /* 如果状态已完成但没 URL，说明后端接口没返回 file_url 字段 */
                <div className="text-center p-8">
                  <p className="text-sm text-slate-600 font-bold mb-2">
                    处理已完成
                  </p>
                  <p className="text-xs text-slate-400">
                    但未能在 API 响应中找到 PDF 文件路径。
                  </p>
                </div>
              ) : (
                <>
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mb-2" />
                  <p className="text-sm text-slate-500">正在提取文档文本...</p>
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PDFViewer;
