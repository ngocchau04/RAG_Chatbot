from abc import ABC, abstractmethod

from app.domain.entities.chat_answer import ChatAnswer
from app.domain.entities.chat_message import ChatMessage


class RagProviderPort(ABC):
    @abstractmethod
    def answer(self, query: str, history: list[ChatMessage]) -> ChatAnswer:
        raise NotImplementedError
