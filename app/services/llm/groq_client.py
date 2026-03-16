from typing import Any

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser

from app.core.config import get_settings
from app.models.api.schemas import SymptomsRequest, AdvisoryResponse, AdvisorySection
from app.services.llm.base import BaseLLMClient
from app.services.llm.prompts import build_prompt


class GroqLLMClient(BaseLLMClient):
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY is not configured.")

        self._model = ChatGroq(
            model=settings.groq_model,
            api_key=settings.groq_api_key,
            temperature=0.4,
        )
        self._chain = build_prompt() | self._model | StrOutputParser()

    async def generate_advisory(self, payload: SymptomsRequest) -> AdvisoryResponse:
        variables: dict[str, Any] = {
            "symptoms": payload.symptoms,
            "age": payload.age or "unknown",
            "sex": payload.sex or "unspecified",
            "duration": payload.duration or "unspecified",
        }
        text = await self._chain.ainvoke(variables)
        return _parse_structured_response(text)


def _parse_structured_response(text: str) -> AdvisoryResponse:
    from app.services.llm.gemini_client import _parse_structured_response as parse

    return parse(text)

