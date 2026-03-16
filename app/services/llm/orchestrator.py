from app.models.api.schemas import SymptomsRequest, AdvisoryResponse
from app.services.llm.base import BaseLLMClient
from app.services.llm.gemini_client import GeminiLLMClient
from app.services.llm.groq_client import GroqLLMClient


class LLMOrchestrator:
    """
    Simple orchestrator that selects the appropriate LLM client
    implementation based on the requested model.
    """

    def _get_client(self, model: str) -> BaseLLMClient:
        if model == "gemini":
            return GeminiLLMClient()
        if model == "groq":
            return GroqLLMClient()
        raise ValueError(f"Unsupported model: {model}")

    async def generate(self, payload: SymptomsRequest) -> AdvisoryResponse:
        client = self._get_client(payload.model)
        return await client.generate_advisory(payload)

