from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import HTTPException

from app.models.api.schemas import SymptomsRequest, AdvisoryResponse, SupportedModel
from app.services.llm.orchestrator import LLMOrchestrator


router = APIRouter()


def get_orchestrator() -> LLMOrchestrator:
    return LLMOrchestrator()


templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": None,
            "error": None,
            "symptoms": "",
            "current_model": "groq",
        },
    )


@router.post("/analyze", response_class=HTMLResponse)
async def analyze_symptoms(
    request: Request,
    orchestrator: LLMOrchestrator = Depends(get_orchestrator),
):
    form = await request.form()
    symptoms = (form.get("symptoms") or "").strip()
    model: SupportedModel = (form.get("model") or "groq").lower()  # type: ignore
    age_raw = (form.get("age") or "").strip()
    sex = (form.get("sex") or "").strip()
    duration = (form.get("duration") or "").strip() or None

    if not age_raw:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": "Age is required.",
                "symptoms": symptoms,
                "current_model": model,
            },
            status_code=status.HTTP_200_OK,
        )

    try:
        age = int(age_raw)
    except ValueError:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": "Age must be a valid integer.",
                "symptoms": symptoms,
                "current_model": model,
            },
            status_code=status.HTTP_200_OK,
        )

    if not sex:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": "Sex is required.",
                "symptoms": symptoms,
                "current_model": model,
            },
            status_code=status.HTTP_200_OK,
        )

    if not symptoms:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": "Please describe your symptoms before submitting.",
                "symptoms": symptoms,
                "current_model": model,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        payload = SymptomsRequest(
            symptoms=symptoms,
            age=age,
            sex=sex,  # type: ignore[arg-type]
            duration=duration,
            model=model,
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": str(exc),
                "symptoms": symptoms,
                "current_model": model,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    try:
        advisory: AdvisoryResponse = await orchestrator.generate(payload)
    except ValueError as ve:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": str(ve),
                "symptoms": symptoms,
                "current_model": model,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        # Surface the underlying LLM error to the UI so it's easier to debug
        # without needing to rebuild Docker each time.
        error_message = f"LLM error: {e}"
        print(error_message)
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": None,
                "error": error_message,
                "symptoms": symptoms,
                "current_model": model,
            },
            status_code=status.HTTP_200_OK,
        )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": advisory,
            "error": None,
            "symptoms": symptoms,
            "current_model": model,
        },
    )

