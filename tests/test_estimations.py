from unittest.mock import AsyncMock, Mock
from uuid import UUID

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers import estimations
from app.services.conversation_store import ConversationStore

SINGLE = "/api/v1/estimate"
MULTI = "/api/v1/conversation/estimate"


def llm_result(estimation="400 horas"):
    return {
        "estimation": estimation,
        "model": "gpt-4o-mini",
        "usage": {"input_tokens": 500, "output_tokens": 200},
    }


@pytest.fixture
def store(monkeypatch):
    instance = ConversationStore()
    monkeypatch.setattr(estimations, "conversation_store", instance)
    return instance


@pytest.fixture
def mock_llm(monkeypatch):
    mock = AsyncMock(return_value=llm_result())
    monkeypatch.setattr(estimations, "generate_estimation", mock)
    monkeypatch.setattr(
        estimations, "get_settings", Mock(return_value=Mock(LLM_PROVIDER="openai"))
    )
    return mock


@pytest.fixture
def client(store, mock_llm):
    app = FastAPI()
    app.include_router(estimations.router)
    with TestClient(app) as test_client:
        yield test_client


def test_single_turn(client, mock_llm, store):
    response = client.post(SINGLE, json={"transcription": "Estima un CRM"})
    assert response.status_code == 200
    assert response.json() == {
        **llm_result(), "provider": "openai", "conversation_id": None,
    }
    mock_llm.assert_awaited_once_with("Estima un CRM")
    assert store.conversations == {}


def test_create_conversation(client, mock_llm, store):
    response = client.post(MULTI, json={"transcription": "Estima un CRM"})
    assert response.status_code == 200
    data = response.json()
    cid = data["conversation_id"]
    assert UUID(cid).version == 4
    assert data == {**llm_result(), "provider": "openai", "conversation_id": cid}
    mock_llm.assert_awaited_once_with(
        transcription="Estima un CRM", conversation_history=[]
    )
    assert store.get(cid).get_messages() == [
        {"role": "user", "content": "Estima un CRM"},
        {"role": "assistant", "content": "400 horas"},
    ]


def test_continue_conversation(client, mock_llm, store):
    first = client.post(MULTI, json={"transcription": "Estima un CRM"})
    cid = first.json()["conversation_id"]
    mock_llm.return_value = llm_result("450 horas")
    response = client.post(MULTI, json={
        "transcription": "Añade testing", "conversation_id": cid,
    })
    assert response.status_code == 200
    assert response.json()["conversation_id"] == cid
    assert response.json()["estimation"] == "450 horas"
    history = [
        {"role": "user", "content": "Estima un CRM"},
        {"role": "assistant", "content": "400 horas"},
    ]
    mock_llm.assert_awaited_with(
        transcription="Añade testing", conversation_history=history
    )
    assert mock_llm.await_count == 2
    assert store.get(cid).get_messages() == [
        *history,
        {"role": "user", "content": "Añade testing"},
        {"role": "assistant", "content": "450 horas"},
    ]


def test_conversations_are_isolated(client, mock_llm, store):
    a = client.post(MULTI, json={"transcription": "Estima un CRM"}).json()
    mock_llm.return_value = llm_result("150 horas")
    b = client.post(MULTI, json={"transcription": "Estima inventario"}).json()
    assert a["conversation_id"] != b["conversation_id"]
    mock_llm.assert_awaited_with(
        transcription="Estima inventario", conversation_history=[]
    )
    client.post(MULTI, json={
        "transcription": "Añade testing", "conversation_id": a["conversation_id"],
    })
    mock_llm.assert_awaited_with(
        transcription="Añade testing",
        conversation_history=[
            {"role": "user", "content": "Estima un CRM"},
            {"role": "assistant", "content": "400 horas"},
        ],
    )
    assert len(store.get(b["conversation_id"]).get_messages()) == 2


def test_sliding_window(client, mock_llm, store):
    cid = store.create()
    conversation = store.get(cid)
    for i in range(12):
        conversation.add_user_message(f"Petición {i}")
        conversation.add_assistant_message(f"Respuesta {i}")
    expected = conversation.get_messages()[-20:]
    response = client.post(MULTI, json={
        "transcription": "Refina la estimación", "conversation_id": cid,
    })
    assert response.status_code == 200
    mock_llm.assert_awaited_once_with(
        transcription="Refina la estimación", conversation_history=expected
    )
    assert len(conversation.get_messages()) == 26


def test_unknown_conversation(client, mock_llm):
    response = client.post(MULTI, json={
        "transcription": "Añade testing", "conversation_id": "invalid-id",
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "Conversación no encontrada"}
    mock_llm.assert_not_awaited()


@pytest.mark.parametrize("endpoint", [SINGLE, MULTI])
@pytest.mark.parametrize("payload", [{}, {"transcription": ""}])
def test_invalid_request(client, mock_llm, endpoint, payload):
    assert client.post(endpoint, json=payload).status_code == 422
    mock_llm.assert_not_awaited()


@pytest.mark.parametrize("endpoint", [SINGLE, MULTI])
def test_provider_error(client, mock_llm, endpoint):
    mock_llm.side_effect = RuntimeError("Error del proveedor")
    response = client.post(endpoint, json={"transcription": "Estima un CRM"})
    assert response.status_code == 502
    assert response.json() == {"detail": "No se pudo generar la estimación"}


def test_failed_refinement_preserves_history(client, mock_llm, store):
    cid = store.create()
    conversation = store.get(cid)
    conversation.add_user_message("Estima un CRM")
    conversation.add_assistant_message("400 horas")
    original = conversation.get_messages()
    mock_llm.side_effect = RuntimeError("Error del proveedor")
    response = client.post(MULTI, json={
        "transcription": "Añade testing", "conversation_id": cid,
    })
    assert response.status_code == 502
    assert conversation.get_messages() == original


def test_missing_usage(client, mock_llm):
    mock_llm.return_value = {**llm_result(), "usage": None}
    response = client.post(SINGLE, json={"transcription": "Estima un CRM"})
    assert response.status_code == 200
    assert response.json()["usage"] is None
