from unittest.mock import AsyncMock, Mock, patch

import pytest

from app.prompts.estimation import build_system_prompt
from app.services.llm_service import generate_estimation


@pytest.fixture
def mock_openai():
    response = Mock(
        choices=[Mock(message=Mock(content="Estimación: 400 horas"))],
        usage=Mock(prompt_tokens=500, completion_tokens=200),
    )
    with (
        patch("app.services.llm_service.AsyncOpenAI") as client,
        patch("app.services.llm_service.get_settings") as settings,
    ):
        settings.return_value = Mock(
            OPENAI_API_KEY="test-api-key", LLM_MODEL="gpt-4o-mini"
        )
        create = AsyncMock(return_value=response)
        client.return_value.chat.completions.create = create
        yield create


@pytest.mark.asyncio
async def test_generate_estimation_single_turn(mock_openai):
    result = await generate_estimation("Estima un CRM")
    assert result == {
        "estimation": "Estimación: 400 horas",
        "model": "gpt-4o-mini",
        "usage": {"input_tokens": 500, "output_tokens": 200},
    }
    mock_openai.assert_awaited_once_with(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": build_system_prompt()},
            {"role": "user", "content": "Estima un CRM"},
        ],
    )


@pytest.mark.asyncio
async def test_generate_estimation_multi_turn(mock_openai):
    history = [
        {"role": "user", "content": "Estima un CRM"},
        {"role": "assistant", "content": "Estimación: 400 horas"},
    ]
    await generate_estimation("Añade testing", conversation_history=history)
    mock_openai.assert_awaited_once_with(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": build_system_prompt()},
            *history,
            {"role": "user", "content": "Añade testing"},
        ],
    )


@pytest.mark.asyncio
async def test_generate_estimation_empty_history(mock_openai):
    await generate_estimation("Estima un CRM", conversation_history=[])
    assert mock_openai.call_args.kwargs["messages"] == [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": "Estima un CRM"},
    ]


@pytest.mark.asyncio
async def test_generate_estimation_does_not_modify_history(mock_openai):
    history = [
        {"role": "user", "content": "Estima un CRM"},
        {"role": "assistant", "content": "400 horas"},
    ]
    original = [message.copy() for message in history]
    await generate_estimation("Añade testing", conversation_history=history)
    assert history == original


@pytest.mark.asyncio
async def test_generate_estimation_token_usage(mock_openai):
    result = await generate_estimation("Estima un CRM")
    assert result["usage"] == {"input_tokens": 500, "output_tokens": 200}


@pytest.mark.asyncio
async def test_generate_estimation_without_usage(mock_openai):
    mock_openai.return_value.usage = None
    result = await generate_estimation("Estima un CRM")
    assert result["usage"] is None


@pytest.mark.asyncio
@pytest.mark.parametrize("content", [None, ""])
async def test_generate_estimation_empty_response(mock_openai, content):
    mock_openai.return_value.choices[0].message.content = content
    with pytest.raises(ValueError, match="El modelo no ha generado una estimación"):
        await generate_estimation("Estima un CRM")


@pytest.mark.asyncio
async def test_generate_estimation_provider_error(mock_openai):
    mock_openai.side_effect = RuntimeError("Error del proveedor")
    with pytest.raises(RuntimeError, match="Error del proveedor"):
        await generate_estimation("Estima un CRM")
