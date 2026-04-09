import io
import time

from openai import OpenAI

from app.application.ports.pdf_rag_provider_port import PdfRagProviderPort
from app.application.ports.rag_provider_port import RagProviderPort
from app.core.config import Settings
from app.domain.entities.chat_answer import ChatAnswer
from app.domain.entities.chat_message import ChatMessage
from app.domain.entities.citation import Citation


class OpenAIResponsesRagProvider(RagProviderPort, PdfRagProviderPort):
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        client_kwargs = {"api_key": settings.openai_api_key, "timeout": 60.0, "max_retries": 2}
        if settings.openai_base_url.strip():
            client_kwargs["base_url"] = settings.openai_base_url.strip()
        self._client = OpenAI(**client_kwargs)

    def answer(self, query: str, history: list[ChatMessage]) -> ChatAnswer:
        input_messages: list[dict[str, str]] = [
            {"role": item.role, "content": item.content}
            for item in history
            if item.content.strip()
        ]
        input_messages.append({"role": "user", "content": query})

        response = self._client.responses.create(
            model=self._settings.openai_model,
            input=input_messages,
            tools=[
                {
                    "type": "file_search",
                    "vector_store_ids": [self._settings.openai_vector_store_id],
                }
            ],
        )
        return self._map_response_to_answer(response=response)

    def answer_with_pdf(self, query: str, filename: str, file_bytes: bytes) -> ChatAnswer:
        file_buffer = io.BytesIO(file_bytes)
        file_buffer.name = filename

        created_file = self._client.files.create(file=file_buffer, purpose="assistants")
        vector_store = self._client.vector_stores.create(name=f"upload-{int(time.time())}")

        try:
            if hasattr(self._client.vector_stores.files, "create_and_poll"):
                self._client.vector_stores.files.create_and_poll(
                    vector_store_id=vector_store.id,
                    file_id=created_file.id,
                )
            else:
                self._client.vector_stores.files.create(
                    vector_store_id=vector_store.id,
                    file_id=created_file.id,
                )
                # Fallback poll when helper is not available in this SDK version.
                for _ in range(30):
                    status = self._client.vector_stores.retrieve(vector_store.id)
                    if status.file_counts.completed and status.file_counts.completed >= 1:
                        break
                    time.sleep(1)

            response = self._client.responses.create(
                model=self._settings.openai_model,
                input=query,
                tools=[
                    {
                        "type": "file_search",
                        "vector_store_ids": [vector_store.id],
                    }
                ],
                tool_choice="required",
            )
            return self._map_response_to_answer(response=response)
        finally:
            try:
                self._client.vector_stores.delete(vector_store.id)
            except Exception:
                pass
            try:
                self._client.files.delete(created_file.id)
            except Exception:
                pass

    def _map_response_to_answer(self, response: object) -> ChatAnswer:
        answer_text = ""
        citations: list[Citation] = []

        for output_item in response.output:
            if output_item.type != "message" or not output_item.content:
                continue
            for content in output_item.content:
                if getattr(content, "type", "") == "output_text":
                    answer_text += getattr(content, "text", "")
                    for ann in getattr(content, "annotations", []) or []:
                        filename = getattr(ann, "filename", "")
                        if filename:
                            citations.append(Citation(filename=filename))

        unique = {c.filename: c for c in citations}
        return ChatAnswer(answer=answer_text.strip(), citations=list(unique.values()))
