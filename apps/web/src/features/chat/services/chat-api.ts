import { ChatMessage, ChatResponse } from "@/shared/types/chat";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "/backend";

export async function askRag(query: string, history: ChatMessage[]): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE}/api/v1/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, history }),
  });

  if (!response.ok) {
    const errorBody = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(errorBody?.detail ?? `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<ChatResponse>;
}

export async function askRagOnPdf(query: string, file: File): Promise<ChatResponse> {
  const form = new FormData();
  form.append("query", query);
  form.append("file", file);

  const response = await fetch(`${API_BASE}/api/v1/chat/file`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const errorBody = (await response.json().catch(() => null)) as { detail?: string } | null;
    throw new Error(errorBody?.detail ?? `Request failed with status ${response.status}`);
  }

  return response.json() as Promise<ChatResponse>;
}
