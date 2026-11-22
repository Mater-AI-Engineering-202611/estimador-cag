from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_estimation():
    # Simulamos la respuesta de OpenAI
    with patch(
        "app.routers.estimations.generate_estimation",
        new_callable=AsyncMock
    ) as mock_llm:

        mock_llm.return_value = "Backend: 40 horas. Frontend: 30 horas."

        response = client.post(
            "/api/v1/estimate",
            json={
                "transcription": "Necesitamos desarrollar una aplicación web para gestionar clientes."
            }
        )

    # Comprobar HTTP 200
    assert response.status_code == 200

    # Comprobar respuesta JSON
    data = response.json()

    assert data["estimation"] == "Backend: 40 horas. Frontend: 30 horas."
    assert data["model"] == "gpt-4o-mini"
    assert data["provider"] == "openai"

    # Verificar que se llamó al servicio con la transcripción
    mock_llm.assert_awaited_once()


def test_estimation_invalid_transcription():
    response = client.post(
        "/api/v1/estimate",
        json={"transcription": "Hola"}
    )

    # Pydantic debe rechazar textos demasiado cortos
    assert response.status_code == 422
