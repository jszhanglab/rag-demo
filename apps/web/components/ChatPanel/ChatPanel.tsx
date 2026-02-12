"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import ReactMarkdown from "react-markdown";

/**
 * Updated SearchHit type to include page and bounding box metadata
 * for PDF navigation and highlighting.
 */
type SearchHit = {
  chunk_id: string;
  distance: number;
  text: string;
  document_id: string;
  chunk_index: number;
  metadata: {
    page: number; // 1-based page index from OCR
    bbox: number[][]; // Coordinates for highlighting [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
  };
};

type Message = {
  role: string;
  content: string; // Contains the LLM generated response
  hits?: SearchHit[]; // Contains the retrieved source chunks
};

type ChatPanelProps = {
  docId: string | null;
};

export default function ChatPanel({ docId }: ChatPanelProps) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  const t = useTranslations("chat");

  /**
   * Dispatches a custom event to notify the PDFViewer to jump to a specific location.
   */
  const handleJumpToSource = (page: any, bbox: number[][]) => {
    console.log("[DEBUG] 完整的 metadata 内容:", page, bbox);
    const pageNum = Number(page);

    if (isNaN(pageNum) || pageNum <= 0) {
      console.warn("[ChatPanel] 无效页码:", page);
      return;
    }

    console.log(`[ChatPanel] 正在发送跳转信号: Page ${pageNum}`);

    const event = new CustomEvent("jumpToPdfLocation", {
      detail: {
        page: pageNum,
        bbox: bbox,
      },
    });

    window.dispatchEvent(event);
  };

  async function handleSend() {
    if (!input.trim() || !docId || isSearching) return;

    const userQuery = input.trim();
    setMessages((prev) => [...prev, { role: "user", content: userQuery }]);
    setInput("");
    setIsSearching(true);

    try {
      const response = await fetch("/api/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          query: userQuery,
          top_k: 8, // Increased top_k for better LLM context
          document_id: docId,
        }),
      });

      if (!response.ok) throw new Error("Search request failed");

      const data = await response.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer,
          hits: data.hits,
        },
      ]);
    } catch (error) {
      console.error("Search Error:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            "Error: Unable to generate response. Please check your connection.",
        },
      ]);
    } finally {
      setIsSearching(false);
    }
  }

  return (
    <div className="h-full flex flex-col bg-slate-50">
      {/* Messages List Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex flex-col ${m.role === "user" ? "items-end" : "items-start"}`}
          >
            {/* Chat Bubble */}
            <div
              className={`max-w-[85%] px-4 py-3 rounded-2xl shadow-sm ${
                m.role === "user"
                  ? "bg-blue-600 text-white rounded-tr-none"
                  : "bg-white text-slate-800 border border-slate-200 rounded-tl-none"
              }`}
            >
              {/* Markdown support for bold text, lists, and structure */}
              <article className="prose prose-sm max-w-none prose-slate">
                <ReactMarkdown>{m.content}</ReactMarkdown>
              </article>
            </div>

            {/* Citations/Sources Section */}
            {m.role === "assistant" && m.hits && m.hits.length > 0 && (
              <div className="mt-3 w-[85%] space-y-2">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider px-1">
                  Reference Sources ({m.hits.length})
                </p>
                <div className="grid grid-cols-1 gap-2">
                  {m.hits.map((hit, idx) => {
                    console.log(`第 ${idx + 1} 个 Source 的完整数据:`, hit);
                    return (
                      <button
                        key={hit.chunk_id}
                        onClick={() =>
                          handleJumpToSource(
                            hit.metadata.page,
                            hit.metadata.bbox,
                          )
                        }
                        className="text-left p-2 bg-white/50 border border-slate-200 rounded-lg text-[11px] text-slate-500 hover:border-blue-400 hover:bg-white transition-all cursor-pointer group"
                        title="Click to view in PDF"
                      >
                        <div className="flex justify-between items-center mb-1">
                          <span className="font-mono text-blue-500 font-bold">
                            SOURCE #{idx + 1}
                          </span>
                          <span className="text-[9px] bg-blue-100 text-blue-600 px-1.5 py-0.5 rounded-full font-bold">
                            PAGE {hit.metadata.page}
                          </span>
                        </div>
                        <p className="line-clamp-2 group-hover:text-slate-800 transition-colors">
                          {hit.text}
                        </p>
                      </button>
                    );
                  })}
                </div>
              </div>
            )}
          </div>
        ))}
        {isSearching && (
          <div className="flex items-center space-x-2 text-slate-400 text-xs italic">
            <div className="w-1.5 h-1.5 bg-slate-300 rounded-full animate-bounce" />
            <span>{t("searching")}</span>
          </div>
        )}
      </div>

      {/* Input Field Section */}
      <div className="p-4 bg-white border-t border-slate-200">
        <div className="flex items-end gap-2 max-w-4xl mx-auto">
          <textarea
            className="flex-1 border border-slate-300 rounded-xl px-4 py-3 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none disabled:opacity-50 resize-none"
            placeholder={docId ? t("placeholder") : t("select_doc_first")}
            rows={1}
            value={input}
            disabled={!docId || isSearching}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
          />
          <button
            onClick={handleSend}
            disabled={!docId || isSearching || !input.trim()}
            className="bg-blue-600 text-white px-5 py-3 rounded-xl hover:bg-blue-700 disabled:bg-slate-300 transition-all font-medium"
          >
            {isSearching ? "..." : t("send_btn")}
          </button>
        </div>
      </div>
    </div>
  );
}
