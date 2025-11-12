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

    // Add user message
    setMessages((prev) => [...prev, { role: "user", content: input }]);

    // Add a mock assistant reply
    const reply = `Mock reply for docId=${docId ?? "none"}, threadId=${
      threadId ?? "none"
    }`;
    setMessages((prev) => [...prev, { role: "assistant", content: reply }]);

    setInput("");
  }

  return (
    <div className="h-full flex flex-col">
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`p-2 rounded border text-sm ${
              m.role === "user" ? "text-right bg-blue-50" : "bg-gray-50"
            }`}
          >
            {m.content}
          </div>
        ))}
      </div>

      <div className="border-t p-2 flex gap-2">
        <textarea
          className="flex-1 border rounded p-2 text-sm h-16"
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
          className="border rounded px-3 text-sm bg-white hover:bg-gray-100"
        >
          Send
        </button>
      </div>
    </div>
  );
}
