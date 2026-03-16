from typing import Any

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

from app.core.config import get_settings
from app.models.api.schemas import SymptomsRequest, AdvisoryResponse, AdvisorySection
from app.services.llm.base import BaseLLMClient
from app.services.llm.prompts import build_prompt


class GeminiLLMClient(BaseLLMClient):
    def __init__(self) -> None:
        settings = get_settings()
        if not settings.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self._model = ChatGoogleGenerativeAI(
            model=settings.gemini_model,
            api_key=settings.gemini_api_key,
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
    """
    Very lightweight parser that expects the model to output four sections with
    headings matching the required structure, but falls back gracefully.
    """
    lower = text.lower()

    def extract_section(title: str) -> str:
        idx = lower.find(title.lower())
        if idx == -1:
            return ""
        # Find next numbered heading or end
        rest = text[idx:]
        for next_title in [
            "2. Precautions",
            "3. Medication Guidance",
            "4. Nutrition Advice",
        ]:
            next_idx = rest.lower().find(next_title.lower())
            if next_idx != -1 and next_idx > 0:
                return rest[:next_idx].strip()
        return rest.strip()

    possible = extract_section("1. Possible Conditions") or "No conditions suggested."
    precautions = extract_section("2. Precautions") or "No specific precautions provided."
    meds = extract_section("3. Medication Guidance") or "No medication guidance provided."
    nutrition = extract_section("4. Nutrition Advice") or "No nutrition advice provided."

    return AdvisoryResponse(
        possible_conditions=AdvisorySection(
            title="Possible Conditions", content=possible
        ),
        precautions=AdvisorySection(title="Precautions", content=precautions),
        medication_guidance=AdvisorySection(
            title="Medication Guidance", content=meds
        ),
        nutrition_advice=AdvisorySection(
            title="Nutrition Advice", content=nutrition
        ),
        raw_text=text,
    )

