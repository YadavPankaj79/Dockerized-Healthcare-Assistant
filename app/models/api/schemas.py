from typing import Literal, Optional
from pydantic import BaseModel, Field, validator


SupportedModel = Literal["gemini", "groq"]


class SymptomsRequest(BaseModel):
    symptoms: str = Field(..., description="Free-text description of symptoms")
    age: int = Field(..., ge=0, le=120, description="Age of the patient")
    sex: Literal["male", "female", "other"] = Field(
        ..., description="Sex of the patient"
    )
    duration: Optional[str] = Field(
        None, description="Approximate duration, e.g. '2 days', '1 week'"
    )
    model: SupportedModel = Field("gemini", description="LLM model to use")

    @validator("symptoms")
    def symptoms_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Symptoms description must not be empty.")
        return v.strip()


class AdvisorySection(BaseModel):
    title: str
    content: str


class AdvisoryResponse(BaseModel):
    possible_conditions: AdvisorySection
    precautions: AdvisorySection
    medication_guidance: AdvisorySection
    nutrition_advice: AdvisorySection
    raw_text: str

