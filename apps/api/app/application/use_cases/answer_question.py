from app.application.ports.rag_provider_port import RagProviderPort
from app.domain.entities.chat_answer import ChatAnswer
from app.domain.entities.chat_message import ChatMessage


class AnswerQuestionUseCase:
    def __init__(self, provider: RagProviderPort) -> None:
        self._provider = provider

    def execute(self, query: str, history: list[ChatMessage]) -> ChatAnswer:
        if not query.strip():
            raise ValueError("Query must not be empty")
        return self._provider.answer(query=query, history=history)
