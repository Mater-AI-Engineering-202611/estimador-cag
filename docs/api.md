# Documentación de la API

## 1. Descripción

API REST desarrollada con FastAPI para generar y refinar estimaciones de proyectos de software utilizando un LLM y contexto CAG.

- URL base: http://localhost:8001
- Swagger UI: http://localhost:8001/docs

## 2. Health Check

### GET /health

Comprueba que el servicio HTTP está disponible. No verifica la conectividad con OpenAI.

```http
GET /health
```

Respuesta HTTP 200:

```json
{
  "status": "healthy"
}
```

## 3. Contrato de estimaciones

Los dos endpoints POST utilizan `Content-Type: application/json` y el mismo esquema de entrada.

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `transcription` | string | Sí | Transcripción inicial o petición de refinamiento; mínimo 1 carácter |
| `conversation_id` | string o null | No | Identificador de una conversación; valor predeterminado null |

La respuesta contiene:

| Campo | Tipo | Descripción |
|---|---|---|
| `estimation` | string | Texto generado por el LLM |
| `model` | string | Modelo configurado |
| `provider` | string | Proveedor configurado |
| `conversation_id` | string o null | Identificador en Multi-turn; null en Single-turn |
| `usage` | objeto o null | Métricas de la llamada actual |
| `usage.input_tokens` | entero no negativo | Tokens de entrada |
| `usage.output_tokens` | entero no negativo | Tokens de salida |

## 4. Generar estimación Single-turn

### POST /api/v1/estimate

Genera una estimación independiente, sin consultar ni almacenar historial. Si se proporciona `conversation_id`, se ignora.

Petición:

```json
{
  "transcription": "El cliente necesita una aplicación web para gestionar empleados, vacaciones y permisos. Requiere autenticación, roles y un panel administrativo."
}
```

Respuesta HTTP 200 (ejemplo orientativo):

```json
{
  "estimation": "Backend: 70 horas. Frontend: 50 horas. Testing: 25 horas. Total: 145 horas. Equipo: 2 desarrolladores. Duración estimada: 2 semanas.",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "conversation_id": null,
  "usage": {
    "input_tokens": 500,
    "output_tokens": 200
  }
}
```

## 5. Generar o refinar estimación Multi-turn

### POST /api/v1/conversation/estimate

#### Iniciar conversación

Omitir `conversation_id` o enviarlo como `null`.

```json
{
  "transcription": "El cliente necesita un CRM web."
}
```

Respuesta HTTP 200 (ejemplo orientativo):

```json
{
  "estimation": "Estimación: 400 horas",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "conversation_id": "8a19c7d2-1234-4567-8901-123456789abc",
  "usage": {
    "input_tokens": 500,
    "output_tokens": 200
  }
}
```

#### Continuar conversación

Utilizar el identificador real devuelto por la petición anterior.

```json
{
  "transcription": "Añade 50 horas de testing y recalcula el total.",
  "conversation_id": "8a19c7d2-1234-4567-8901-123456789abc"
}
```

Respuesta HTTP 200 (ejemplo orientativo):

```json
{
  "estimation": "Estimación actualizada: 450 horas",
  "model": "gpt-4o-mini",
  "provider": "openai",
  "conversation_id": "8a19c7d2-1234-4567-8901-123456789abc",
  "usage": {
    "input_tokens": 750,
    "output_tokens": 220
  }
}
```

El identificador se mantiene durante los refinamientos. El modelo recibe hasta 10 turnos anteriores y la petición actual. Las estimaciones y los tokens de los ejemplos son simulados; las respuestas reales pueden variar.

## 6. Posibles errores

| Código | Descripción |
|---|---|
| 200 | Respuesta correcta |
| 404 | Identificador inexistente en Multi-turn |
| 422 | Datos de entrada inválidos según Pydantic |
| 502 | Error durante la generación o construcción de la respuesta |

Ejemplo HTTP 404:

```json
{"detail": "Conversación no encontrada"}
```

Ejemplo HTTP 502:

```json
{"detail": "No se pudo generar la estimación"}
```

## 7. Probar desde Swagger

1. Acceder a http://localhost:8001/docs.
2. Seleccionar el endpoint deseado y pulsar `Try it out`.
3. Introducir el JSON y pulsar `Execute`.
4. Revisar el código HTTP y la respuesta.
5. En Multi-turn, copiar el identificador devuelto y utilizarlo en la siguiente petición.

## 8. Arquitectura de la petición

1. FastAPI recibe la petición y Pydantic valida los datos.
2. En Multi-turn, el router crea o recupera la conversación y obtiene la ventana de historial.
3. El servicio construye los mensajes con el System Prompt, ejemplos CAG, historial opcional y petición actual.
4. Se realiza la llamada asíncrona a OpenAI.
5. En Multi-turn, se almacena el nuevo par usuario/asistente tras recibir la respuesta.
6. Se devuelve la respuesta JSON.

## 9. Consideraciones

- Las llamadas reales requieren una API Key válida y pueden generar costes.
- Las métricas de tokens son por llamada y pueden ser null.
- El historial reside en RAM y se pierde al reiniciar el proceso.
- Los ejemplos CAG se incluyen en cada petición.
- Las estimaciones son orientativas y requieren revisión humana.
