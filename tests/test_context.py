from app.context.examples import ESTIMATION_EXAMPLES
from app.services.llm_service import build_system_prompt


def test_context_has_two_examples():
    """Verificar que existen al menos dos ejemplos."""
    assert len(ESTIMATION_EXAMPLES) >= 2


def test_system_prompt_includes_examples():
    """Verificar que los ejemplos se inyectan en el prompt."""
    prompt = build_system_prompt()

    for example in ESTIMATION_EXAMPLES:
        assert example["meeting_summary"] in prompt
        assert example["estimation"] in prompt


def test_system_prompt_has_instructions():
    """Verificar que el modelo recibe instrucciones."""
    prompt = build_system_prompt()

    assert "experto en estimación" in prompt
    assert "horas" in prompt
