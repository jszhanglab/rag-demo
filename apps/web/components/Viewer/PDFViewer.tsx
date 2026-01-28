"use client";

import React from "react";
import useSWR from "swr";
import { buildDocumentDetailUrl } from "@/constants/apiRouteBuilders";
import { useTranslations } from "next-intl";

type DocumentDetail = {
  id?: string;
  status: string; // DocumentStatus
  ocr_text?: string | null;
  error_message?: string | null;
};

interface PDFViewerProps {
  docId: string | null;
}

const fetcher = async (url: string): Promise<DocumentDetail> => {
  const res = await fetch(url, {
    headers: { Accept: "application/json" },
  });
  if (!res.ok) {
    throw new Error(`Failed to fetch document detail: ${res.status}`);
  }
  return res.json();
};

const isTerminalStatus = (status?: string) =>
  status === "EMBEDDING_DONE" || status === "FAILED";

const PDFViewer: React.FC<PDFViewerProps> = ({ docId }) => {
  const i18n_fileStatus = useTranslations("fileProcessStatus");

  const getStatusLabel = (status?: string) => {
    switch (status) {
      case "UPLOADED":
        return i18n_fileStatus("uploaded");
      case "OCR_PROCESSING":
        return i18n_fileStatus("ocr_processing");
      case "OCR_DONE":
        return i18n_fileStatus("ocr_done");
      case "CHUNK_DONE":
        return i18n_fileStatus("chunk_done");
      case "EMBEDDING_PROCESSING":
        return i18n_fileStatus("embedding_processing");
      case "EMBEDDING_DONE":
        return i18n_fileStatus("embedding_done");
      case "FAILED":
        return i18n_fileStatus("failed");
      default:
        return status ? `${status}` : i18n_fileStatus("default");
    }
  };

  const url = docId ? buildDocumentDetailUrl(docId) : null;

  // Polling
  const { data, error, isLoading, mutate } = useSWR(url, fetcher, {
    refreshInterval: (latest) => (isTerminalStatus(latest?.status) ? 0 : 2000),
    revalidateOnFocus: false,
    keepPreviousData: true,
  });

  if (!docId) {
    return <div className="text-slate-500">请选择文件</div>;
  }

  if (error) {
    return (
      <div className="p-4 space-y-3">
        <div className="text-red-600 text-sm">
          获取文档详情失败：
          {error instanceof Error ? error.message : String(error)}
        </div>
        <button
          type="button"
          className="px-3 py-1 rounded-md border text-sm hover:bg-slate-50"
          onClick={() => mutate()}
        >
          重试
        </button>
      </div>
    );
  }

  const status = data?.status;
  const statusLabel = getStatusLabel(status);
  const ocrText = data?.ocr_text ?? null;

  return (
    <div className="h-full flex flex-col gap-4">
      {/* 顶部状态条 */}
      <div className="border rounded-xl bg-white px-4 py-3 text-sm text-slate-700">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <span className="font-medium">Doc</span>
            <span className="text-slate-600">{docId}</span>
            <span className="text-slate-300">|</span>
            <span className="font-medium">Page</span>
          </div>
          <div className="text-slate-800">{statusLabel}</div>
        </div>

        {/* 失败原因 */}
        {status === "FAILED" && data?.error_message ? (
          <div className="mt-2 text-red-600">{data.error_message}</div>
        ) : null}
      </div>

      {/* 内容区 */}
      <div className="flex-1 border rounded-xl bg-white p-4 overflow-auto">
        <h2 className="text-base font-medium text-slate-800 mb-3">OCR Text</h2>

        {/* 处理中/空内容 */}
        {!ocrText ? (
          <div className="text-slate-500 text-sm">
            {isLoading
              ? "正在加载…"
              : status === "UPLOADED" || status === "OCR_PROCESSING"
                ? "OCR 结果尚未生成，请稍候（页面会自动刷新）…"
                : status === "FAILED"
                  ? "没有可显示的 OCR 文本。"
                  : "暂无 OCR 文本。"}
          </div>
        ) : (
          <pre className="whitespace-pre-wrap text-sm text-slate-800 leading-6">
            {ocrText}
          </pre>
        )}
      </div>
    </div>
  );
};

export default PDFViewer;
