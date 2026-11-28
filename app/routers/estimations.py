from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.schemas.estimation import EstimationRequest, EstimationResponse
from app.services.llm_service import generate_estimation
from app.services.conversation_store import conversation_store

router = APIRouter(
    prefix="/api/v1", 
    tags=["Estimaciones"]
)

@router.post("/estimate", response_model=EstimationResponse)
async def create_estimation(request: EstimationRequest):
    """Genera una estimación independiente (Single-turn)."""

    try:
        result = await generate_estimation(request.transcription)

        return EstimationResponse(
            estimation=result["estimation"],
            model=result["model"],
            provider=get_settings().LLM_PROVIDER,
            usage=result["usage"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="No se pudo generar la estimación",
        ) from exc

@router.post("/conversation/estimate", response_model=EstimationResponse)
async def create_conversational_estimation(request: EstimationRequest,):
    """Genera o refina una estimación (Multi-turn)."""

    conversation_id = request.conversation_id

    # 1. Crear una conversación si no existe identificador
    if conversation_id is None:
        conversation_id = conversation_store.create()

    # 2. Validar que la conversación existe
    if not conversation_store.exists(conversation_id):
        raise HTTPException(
            status_code=404,
            detail="Conversación no encontrada",
        )

    # 3. Recuperar la conversación
    conversation = conversation_store.get(conversation_id)

    # 4. Recuperar el historial mediante Sliding Window
    history = conversation.get_messages_windowed(max_turns=10)

    try:
        # 5. Generar la estimación con el historial
        result = await generate_estimation(
            transcription=request.transcription,
            conversation_history=history,
        )

        # 6. Almacenar el nuevo turno
        conversation.add_user_message(request.transcription)
        conversation.add_assistant_message(result["estimation"])

        # 7. Devolver la respuesta
        return EstimationResponse(
            estimation=result["estimation"],
            model=result["model"],
            provider=get_settings().LLM_PROVIDER,
            conversation_id=conversation_id,
            usage=result["usage"],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail="No se pudo generar la estimación",
        ) from exc
