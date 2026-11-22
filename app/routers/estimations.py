from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.schemas.estimation import EstimationRequest, EstimationResponse
from app.services.llm_service import generate_estimation

router = APIRouter(prefix="/api/v1", tags=["Estimaciones"])


@router.post("/estimate", response_model=EstimationResponse)
async def create_estimation(request: EstimationRequest):
    try:
        estimation = await generate_estimation(request.transcription)
        settings = get_settings()

        return EstimationResponse(
            estimation=estimation,
            model=settings.LLM_MODEL,
            provider=settings.LLM_PROVIDER,
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="No se pudo generar la estimación"
        )
