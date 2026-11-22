from fastapi.testclient import TestClient

from app.main import app

# Cliente para probar nuestra API sin arrancar Uvicorn
client = TestClient(app)


def test_health_check():
    # Ejecutar petición GET
    response = client.get("/health")

    # Comprobar código HTTP
    assert response.status_code == 200

    # Comprobar contenido JSON
    assert response.json() == {
        "status": "healthy"
    }
