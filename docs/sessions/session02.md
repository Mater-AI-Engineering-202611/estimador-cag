# Sesión 02 — Scaffolding del proyecto FastAPI y evolución Multi-turn

## 1. Objetivo

Construir un servicio REST con FastAPI capaz de recibir la transcripción de una reunión y generar una estimación de desarrollo de software mediante un LLM.

Se utiliza CAG, incorporando ejemplos estáticos de estimaciones anteriores directamente al contexto del modelo. La evolución de la práctica permite refinar estimaciones mediante conversaciones Multi-turn.

## 2. Tecnologías utilizadas

- Python 3.11 o superior.
- FastAPI, Pydantic y pydantic-settings.
- OpenAI SDK (AsyncOpenAI), con gpt-4o-mini como modelo predeterminado.
- uv para gestión de dependencias.
- pytest, pytest-asyncio y HTTPX para pruebas.
- Ruff para calidad del código.
- GitHub Actions para integración continua.

## 3. Implementación realizada

### Scaffolding inicial

- `routers/`: endpoints HTTP.
- `schemas/`: validación de entrada y salida.
- `services/`: integración con OpenAI y gestión conversacional.
- `context/`: ejemplos estáticos de estimaciones.
- `prompts/`: construcción del System Prompt, separada del servicio.
- `config.py`: configuración mediante variables de entorno.
- `main.py`: inicialización de FastAPI.

### Arquitectura CAG

Se mantienen dos ejemplos de estimaciones previas. El System Prompt contiene instrucciones, ejemplos de referencia y el formato de salida. La transcripción se envía como mensaje de usuario.

No se utilizan bases de datos ni mecanismos de recuperación documental.

### Evolución Multi-turn

El servicio `generate_estimation()` admite un historial opcional. El router decide si debe utilizarlo.

`ConversationStore` identifica conversaciones mediante UUID y las almacena en memoria. `ConversationManager` mantiene los mensajes con roles `user` y `assistant`.

La Sliding Window recupera hasta los últimos 10 turnos previos. El System Prompt se incorpora en cada llamada y no se almacena en el historial. El nuevo par usuario/asistente se guarda después de obtener la respuesta del LLM.

### Endpoints

| Método y ruta | Finalidad |
|---|---|
| `GET /health` | Comprobar el estado del servicio |
| `POST /api/v1/estimate` | Generar una estimación independiente |
| `POST /api/v1/conversation/estimate` | Crear o refinar una estimación conversacional |

Las respuestas de estimación incluyen modelo, proveedor, identificador de conversación opcional y métricas de tokens cuando están disponibles.

## 4. Verificación funcional

```powershell
uv run uvicorn app.main:app --reload --port 8001
```

En la práctica inicial se comprobó el arranque de FastAPI, Swagger, el endpoint `/health` y la generación real de una estimación JSON mediante OpenAI.

Para validar la evolución Multi-turn desde Swagger (`http://localhost:8001/docs`):

1. Ejecutar una estimación Single-turn.
2. Iniciar una conversación sin identificador.
3. Recuperar el `conversation_id` de la respuesta.
4. Enviar una petición de refinamiento con el mismo identificador.
5. Comprobar que se mantiene el contexto y se devuelve la estimación actualizada.

Estas comprobaciones de la nueva rama quedan pendientes de confirmar mediante ejecución real.

## 5. Pruebas automatizadas

La práctica inicial obtuvo un resultado local de 6 tests superados.

La suite ampliada contiene los siguientes casos previstos:

| Fichero | Casos |
|---|---:|
| `test_context.py` | 3 |
| `test_conversation_manager.py` | 8 |
| `test_conversation_store.py` | 7 |
| `test_estimations.py` | 14 |
| `test_llm_service.py` | 9 |
| `test_main.py` | 1 |
| **Total** | **42** |

Se utilizan mocks para verificar la integración técnica sin consumir tokens de OpenAI. Se comprueban el historial, la ventana, el aislamiento, los contratos HTTP, la construcción de mensajes y el tratamiento de errores.

```powershell
uv run python -m pytest -v
```

El resultado de la suite ampliada queda pendiente de verificar.

## 6. Integración continua

El workflow existente se encuentra en `.github/workflows/ci.yml`, preparado originalmente para eventos `push` y `pull_request`.

Debe comprobarse que instala las dependencias de desarrollo y ejecuta la suite actualizada, incluyendo pytest-asyncio. La validación de la rama en GitHub Actions queda pendiente de confirmar.

## 7. Seguridad

La API Key se configura mediante `.env`, excluido del control de versiones. `.env.example` sirve como plantilla.

El identificador de conversación no constituye un mecanismo de autenticación. Las instrucciones del System Prompt tampoco garantizan protección frente a prompt injection.

## 8. Resultado del ejercicio

La implementación cubre el scaffolding inicial, el contexto CAG, la comunicación asíncrona con el LLM, Single-turn, Multi-turn, historial en memoria, Sliding Window y métricas de tokens.

El alcance funcional de la práctica se considera completo a nivel de implementación, pendiente de las comprobaciones finales de ejecución.

## 9. Próximos pasos

Ejecutar la suite completa, verificar ambos modos desde Swagger, validar GitHub Actions e integrar la rama. No se requieren nuevas funcionalidades para cerrar esta práctica.
