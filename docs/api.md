# Documentación de la API

## 1. Descripción

API REST desarrollada con FastAPI para generar estimaciones de proyectos de software utilizando un LLM y arquitectura CAG.

**URL base:** http://localhost:8001

**Swagger UI:** http://localhost:8001/docs

## 2. Health Check

### GET /health

Comprueba que el servicio está disponible.

**Petición:**

```http
GET http://localhost:8001/health
```

**Respuesta HTTP 200:**

```json
{
  "status": "healthy"
}
```

## 3. Generar estimación

### POST /api/v1/estimate

Recibe una transcripción de reunión y genera una estimación de desarrollo de software.

### Request

**Content-Type:** application/json

```json
{
  "transcription": "El cliente necesita una aplicación web para gestionar empleados, vacaciones y permisos. Requiere autenticación, roles y un panel administrativo."
}
```

### Response

**HTTP 200 — Ejemplo orientativo:**

```json
{
  "estimation": "Backend: 70 horas. Frontend: 50 horas. Testing: 25 horas.",
  "model": "gpt-4o-mini",
  "provider": "openai"
}
```

La estimación es generada dinámicamente por el LLM, por lo que puede variar entre peticiones.

## 4. Posibles errores

| Código | Descripción |
|--------|-------------|
| 200 | Estimación generada correctamente |
| 422 | Datos de entrada inválidos |
| 502 | Error durante la generación con el LLM |

## 5. Probar desde Swagger

1. Acceder a http://localhost:8001/docs
2. Seleccionar `POST /api/v1/estimate`.
3. Pulsar `Try it out`.
4. Introducir una transcripción en formato JSON.
5. Pulsar `Execute`.
6. Revisar la respuesta del servidor.

## 6. Arquitectura de la petición

El endpoint utiliza el siguiente flujo:

1. FastAPI recibe la petición HTTP.
2. Pydantic valida la transcripción.
3. El servicio construye el system prompt.
4. Se incorporan los ejemplos estáticos CAG.
5. Se realiza la llamada al modelo de OpenAI.
6. Se devuelve la estimación en formato JSON.

## 7. Consideraciones

- El endpoint necesita una API Key válida.
- Las llamadas reales a OpenAI pueden generar costes.
- Las estimaciones son orientativas.
- No se almacena información en una base de datos.
- Los ejemplos CAG se incluyen en cada petición al LLM.
