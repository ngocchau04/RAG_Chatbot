from pydantic import BaseModel, Field


class ChatMessageDTO(BaseModel):
    role: str = Field(pattern="^(user|assistant|system)$")
    content: str


class ChatRequestDTO(BaseModel):
    query: str
    history: list[ChatMessageDTO] = []


class CitationDTO(BaseModel):
    filename: str


class ChatResponseDTO(BaseModel):
    answer: str
    citations: list[CitationDTO]
