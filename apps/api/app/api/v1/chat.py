from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from openai import APIConnectionError, APIError, OpenAI

from app.api.v1.dependencies import (
    get_answer_question_on_pdf_use_case,
    get_answer_question_use_case,
)
from app.application.use_cases.answer_question_on_pdf import AnswerQuestionOnPdfUseCase
from app.application.use_cases.answer_question import AnswerQuestionUseCase
from app.core.config import Settings, get_settings
from app.domain.entities.chat_message import ChatMessage
from app.presentation.schemas.chat import ChatRequestDTO, ChatResponseDTO, CitationDTO

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponseDTO)
def chat(
    payload: ChatRequestDTO,
    use_case: AnswerQuestionUseCase = Depends(get_answer_question_use_case),
) -> ChatResponseDTO:
    try:
        history = [ChatMessage(role=item.role, content=item.content) for item in payload.history]
        result = use_case.execute(query=payload.query, history=history)
        return ChatResponseDTO(
            answer=result.answer,
            citations=[CitationDTO(filename=item.filename) for item in result.citations],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except APIConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to OpenAI API. Check internet/proxy and OPENAI_API_KEY.",
        ) from exc
    except APIError as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(exc)}") from exc


@router.post("/file", response_model=ChatResponseDTO)
async def chat_on_pdf(
    query: str = Form(...),
    file: UploadFile = File(...),
    use_case: AnswerQuestionOnPdfUseCase = Depends(get_answer_question_on_pdf_use_case),
) -> ChatResponseDTO:
    try:
        file_bytes = await file.read()
        result = use_case.execute(query=query, filename=file.filename or "uploaded.pdf", file_bytes=file_bytes)
        return ChatResponseDTO(
            answer=result.answer,
            citations=[CitationDTO(filename=item.filename) for item in result.citations],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except APIConnectionError as exc:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to OpenAI API. Check internet/proxy and OPENAI_API_KEY.",
        ) from exc
    except APIError as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(exc)}") from exc


@router.get("/openai-health")
def openai_health(settings: Settings = Depends(get_settings)) -> dict[str, str]:
    try:
        kwargs = {"api_key": settings.openai_api_key, "timeout": 20.0, "max_retries": 0}
        if settings.openai_base_url.strip():
            kwargs["base_url"] = settings.openai_base_url.strip()
        client = OpenAI(**kwargs)
        client.models.list()
        return {"status": "ok", "provider": "openai"}
    except APIConnectionError as exc:
        raise HTTPException(status_code=503, detail=f"OpenAI connection failed: {str(exc)}") from exc
    except APIError as exc:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(exc)}") from exc
