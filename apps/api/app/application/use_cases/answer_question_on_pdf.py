from app.application.ports.pdf_rag_provider_port import PdfRagProviderPort
from app.domain.entities.chat_answer import ChatAnswer


class AnswerQuestionOnPdfUseCase:
    def __init__(self, provider: PdfRagProviderPort) -> None:
        self._provider = provider

    def execute(self, query: str, filename: str, file_bytes: bytes) -> ChatAnswer:
        if not query.strip():
            raise ValueError("Query must not be empty")
        if not filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are supported")
        if not file_bytes:
            raise ValueError("File content is empty")
        return self._provider.answer_with_pdf(query=query, filename=filename, file_bytes=file_bytes)
