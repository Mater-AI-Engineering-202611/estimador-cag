# Arquitectura del proyecto

## 1. Descripción

El proyecto implementa una API REST con FastAPI que genera estimaciones de desarrollo de software a partir de transcripciones de reuniones.

Utiliza arquitectura CAG (Cache-Augmented Generation), inyectando ejemplos estáticos directamente en el prompt del modelo LLM.

## 2. Flujo de funcionamiento

1. El cliente envía una transcripción mediante una petición HTTP.
2. FastAPI recibe y valida la petición con Pydantic.
3. El servicio LLM construye el prompt.
4. Se incorporan ejemplos de estimaciones anteriores.
5. Se envía la petición a OpenAI.
6. El modelo genera una estimación.
7. La API devuelve la respuesta en formato JSON.

## 3. Componentes

- `app/main.py`: inicialización de FastAPI.
- `app/config.py`: configuración y variables de entorno.
- `app/routers/estimations.py`: endpoint de estimaciones.
- `app/schemas/estimation.py`: modelos de entrada y salida.
- `app/services/llm_service.py`: integración con el LLM.
- `app/context/examples.py`: ejemplos estáticos para CAG.

## 4. Arquitectura CAG

Los ejemplos de estimaciones anteriores se incorporan directamente al system prompt en cada petición.

No se utiliza base de datos, almacenamiento persistente ni búsqueda vectorial.

## 5. Evolución futura

En próximas sesiones se podrán incorporar:

- Mejora de prompts.
- Más ejemplos de estimaciones.
- Evaluación de respuestas.
- Arquitectura RAG.
- Persistencia de información.
