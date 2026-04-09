from abc import ABC, abstractmethod

from app.domain.entities.chat_answer import ChatAnswer


class PdfRagProviderPort(ABC):
    @abstractmethod
    def answer_with_pdf(self, query: str, filename: str, file_bytes: bytes) -> ChatAnswer:
        raise NotImplementedError
