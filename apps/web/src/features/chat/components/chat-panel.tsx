"use client";

import { FormEvent, useState } from "react";

import { askRag, askRagOnPdf } from "@/features/chat/services/chat-api";
import { ChatMessage } from "@/shared/types/chat";

export function ChatPanel() {
  const [question, setQuestion] = useState("");
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    if (!question.trim() || loading) return;

    const nextHistory: ChatMessage[] = [...messages, { role: "user", content: question.trim() }];
    setMessages(nextHistory);
    setQuestion("");
    setLoading(true);

    try {
      const result = pdfFile
        ? await askRagOnPdf(question.trim(), pdfFile)
        : await askRag(question.trim(), nextHistory);
      const citationText =
        result.citations.length > 0
          ? `\n\nNguon: ${result.citations.map((item) => item.filename).join(", ")}`
          : "";
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `${result.answer}${citationText}`.trim() },
      ]);
    } catch (error) {
      const message = error instanceof Error ? error.message : "Khong the tra loi luc nay. Vui long thu lai.";
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: message },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section style={{ maxWidth: 900, margin: "32px auto", fontFamily: "ui-sans-serif" }}>
      <h1>RAG Chatbot</h1>
      <form onSubmit={onSubmit} style={{ display: "flex", gap: 8, marginTop: 16 }}>
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Hoi du lieu noi bo..."
          style={{ flex: 1, padding: 10, border: "1px solid #ccc", borderRadius: 8 }}
        />
        <button type="submit" disabled={loading} style={{ padding: "10px 16px" }}>
          {loading ? "Dang xu ly..." : "Gui"}
        </button>
      </form>
      <div style={{ marginTop: 12 }}>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setPdfFile(e.target.files?.[0] ?? null)}
        />
        <p style={{ marginTop: 8, color: "#666" }}>
          {pdfFile
            ? `Dang hoi tren file: ${pdfFile.name}`
            : "Chua chon file. He thong se dung vector store mac dinh."}
        </p>
      </div>

      <div style={{ marginTop: 20, display: "grid", gap: 12 }}>
        {messages.map((m, idx) => (
          <article
            key={`${m.role}-${idx}`}
            style={{
              padding: 12,
              borderRadius: 8,
              background: m.role === "user" ? "#eef6ff" : "#f5f5f5",
            }}
          >
            <strong>{m.role === "user" ? "Ban" : "Bot"}:</strong> {m.content}
          </article>
        ))}
      </div>
    </section>
  );
}
