"use client";
import { useState } from "react";

type ChatPanelProps = {
  docId: string | null;
  threadId: string | null;
};

export default function ChatPanel({ docId, threadId }: ChatPanelProps) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<{ role: string; content: string }[]>(
    []
  );

  function handleSend() {
    if (!input.trim()) return;

    setMessages((prev) => [...prev, { role: "user", content: input }]);

    const reply = `Mock reply for docId=${docId ?? "none"}, threadId=${
      threadId ?? "none"
    }`;
    setMessages((prev) => [...prev, { role: "assistant", content: reply }]);

    setInput("");
  }

  return (
    <div className="h-full flex flex-col bg-white">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`text-sm max-w-[80%] p-2 rounded-md ${
              m.role === "user"
                ? "ml-auto bg-blue-100 text-blue-900"
                : "bg-slate-100 text-slate-800"
            }`}
          >
            {m.content}
          </div>
        ))}
      </div>

      {/* Input area */}
      <div className="border-t border-slate-200 bg-white p-3 flex gap-2 items-center">
        <textarea
          className="
            flex-1 
            border border-slate-300 
            rounded-md 
            px-3 py-2 
            text-sm 
            resize-none 
            h-16
            focus:outline-none 
            focus:ring-2 
            focus:ring-slate-400
          "
          placeholder="Type a message..."
          value={input}
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
          className="
            border border-slate-300 
            rounded-md 
            px-4 py-2 
            text-sm 
            bg-white 
            hover:bg-slate-100 
            transition-colors
          "
        >
          Send
        </button>
      </div>
    </div>
  );
}
