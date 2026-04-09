from fastapi import Depends

from app.application.use_cases.answer_question_on_pdf import AnswerQuestionOnPdfUseCase
from app.application.use_cases.answer_question import AnswerQuestionUseCase
from app.core.config import Settings, get_settings
from app.infrastructure.openai.responses_rag_provider import OpenAIResponsesRagProvider


def get_answer_question_use_case(settings: Settings = Depends(get_settings)) -> AnswerQuestionUseCase:
    provider = OpenAIResponsesRagProvider(settings=settings)
    return AnswerQuestionUseCase(provider=provider)


def get_answer_question_on_pdf_use_case(
    settings: Settings = Depends(get_settings),
) -> AnswerQuestionOnPdfUseCase:
    provider = OpenAIResponsesRagProvider(settings=settings)
    return AnswerQuestionOnPdfUseCase(provider=provider)
