export type ChatMessage = {
  role: "user" | "assistant" | "system";
  content: string;
};

export type Citation = {
  filename: string;
};

export type ChatResponse = {
  answer: string;
  citations: Citation[];
};
