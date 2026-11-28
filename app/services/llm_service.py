from openai import AsyncOpenAI

from app.config import get_settings
from app.prompts.estimation import build_system_prompt

async def generate_estimation(
    transcription: str,
    conversation_history: list | None = None,
) -> dict:
    """Genera una estimación en modo Single-turn o Multi-turn."""
    
    settings = get_settings()
    client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    messages = [
        {
            "role": "system",
            "content": build_system_prompt(),
        }
    ]

    if conversation_history:
         messages.extend(conversation_history)

    messages.append({
         "role": "user",
         "content": transcription,
    })

    response = await client.chat.completions.create(
        model=settings.LLM_MODEL,
          messages=messages,
    )

    estimation = response.choices[0].message.content

    if not estimation:
        raise ValueError("El modelo no ha generado una estimación")

    return {
        "estimation": estimation,
        "model": settings.LLM_MODEL,
        "usage": {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
        } if response.usage else None,
    }
