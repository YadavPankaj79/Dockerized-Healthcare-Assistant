from abc import ABC, abstractmethod
from app.models.api.schemas import SymptomsRequest, AdvisoryResponse


class BaseLLMClient(ABC):
    @abstractmethod
    async def generate_advisory(self, payload: SymptomsRequest) -> AdvisoryResponse:
        raise NotImplementedError

