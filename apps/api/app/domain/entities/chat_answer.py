from dataclasses import dataclass

from app.domain.entities.citation import Citation


@dataclass(frozen=True)
class ChatAnswer:
    answer: str
    citations: list[Citation]
