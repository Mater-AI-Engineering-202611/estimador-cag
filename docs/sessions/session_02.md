# Sesión 02 — Scaffolding del proyecto FastAPI

## 1. Objetivo

Construir desde cero un servicio REST con FastAPI capaz de recibir la transcripción de una reunión y generar una estimación de desarrollo de software mediante un modelo LLM.

Se utiliza arquitectura CAG, incorporando ejemplos estáticos de estimaciones anteriores directamente en el prompt.

## 2. Tecnologías utilizadas

- Python 3.11
- FastAPI
- Pydantic y pydantic-settings
- OpenAI (gpt-4o-mini)
- uv para gestión de dependencias
- Pytest para pruebas automatizadas
- GitHub Actions para integración continua

## 3. Implementación realizada

### Estructura del proyecto

Se ha organizado la aplicación separando responsabilidades:

- `routers/`: endpoints HTTP.
- `schemas/`: validación de entrada y salida.
- `services/`: lógica de integración con OpenAI.
- `context/`: ejemplos estáticos de estimaciones.
- `config.py`: configuración mediante variables de entorno.
- `main.py`: inicialización de FastAPI.

### Arquitectura CAG

Se han definido dos ejemplos de estimaciones previas.

El servicio construye un system prompt que contiene:

1. Instrucciones para actuar como estimador de software.
2. Ejemplos de estimaciones anteriores.
3. Indicaciones sobre el formato de la estimación.

La transcripción se envía como mensaje de usuario.

No se utilizan bases de datos ni mecanismos de recuperación documental.

### Endpoints

**GET /health**

Comprueba el estado del servicio.

**POST /api/v1/estimate**

Recibe una transcripción y devuelve una estimación generada por OpenAI.

## 4. Verificación funcional

Se ha ejecutado el servicio localmente mediante:

```powershell
uv run uvicorn app.main:app --reload --port 8001
```

Se ha comprobado:

- El arranque correcto de FastAPI.
- La disponibilidad de Swagger.
- La respuesta del endpoint `/health`.
- La generación real de una estimación mediante OpenAI.
- La devolución de la estimación en formato JSON.

## 5. Pruebas automatizadas

Se han implementado seis pruebas unitarias:

1. Funcionamiento del endpoint de salud.
2. Generación de estimaciones utilizando mocks.
3. Validación de transcripciones inválidas.
4. Existencia de al menos dos ejemplos CAG.
5. Inclusión de ejemplos en el system prompt.
6. Presencia de instrucciones en el system prompt.

Comando de ejecución:

```powershell
uv run python -m pytest -v
```

**Resultado local obtenido: 6 tests superados.**

## 6. Integración continua

Se ha configurado un workflow de GitHub Actions en:

`.github/workflows/ci.yml`

El pipeline está preparado para ejecutarse en eventos `push` y `pull_request`.

Comprueba:

- Instalación de dependencias.
- Existencia de archivos principales.
- Ejecución de pruebas automatizadas.

La ejecución en GitHub Actions queda pendiente de verificar tras publicar el repositorio.

## 7. Seguridad

La API Key de OpenAI se configura mediante variables de entorno.

El archivo `.env` está excluido del control de versiones mediante `.gitignore`.

El repositorio incluye `.env.example` como plantilla de configuración.

## 8. Resultado del ejercicio

Se ha desarrollado una aplicación funcional que implementa el flujo:

Transcripción → FastAPI → Contexto CAG → OpenAI → Estimación JSON

Se ha completado el scaffolding inicial, incorporando adicionalmente pruebas automatizadas, integración continua y documentación técnica.

## 9. Próximos pasos

En las siguientes sesiones se podrá evolucionar el proyecto mediante:

- Mejora de los ejemplos de contexto.
- Optimización del system prompt.
- Evaluación de la calidad de las estimaciones.
- Incorporación de nuevas funcionalidades.
- Evolución hacia una arquitectura RAG.
