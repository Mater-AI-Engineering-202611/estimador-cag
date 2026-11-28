from pydantic import BaseModel, Field

class EstimationRequest(BaseModel):
    """Contrato de entrada para generar o refinar estimaciones."""

    transcription: str = Field(
        min_length=1,
        description="Transcripción inicial o petición de refinamiento"
    )

    conversation_id: str | None = Field(
        default=None,
        description="Identificador de una conversación existente",
    )


class TokenUsage(BaseModel):
    """Métricas de consumo de tokens del LLM."""

    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)

class EstimationResponse(BaseModel):
    """Contrato de salida del servicio de estimaciones."""
    
    estimation: str
    model: str
    provider: str
    conversation_id: str | None = None
    usage: TokenUsage | None = None