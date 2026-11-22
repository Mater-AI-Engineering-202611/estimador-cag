# Estimador de Software con IA — CAG

API REST desarrollada con FastAPI que genera estimaciones de proyectos de software a partir de transcripciones de reuniones utilizando inteligencia artificial.

Proyecto desarrollado durante el Máster de AI Engineering.

## Tecnologías

- Python 3.11+
- FastAPI
- OpenAI (gpt-4o-mini)
- Pydantic
- uv
- Pytest
- GitHub Actions

## Arquitectura

El proyecto utiliza CAG (Cache-Augmented Generation).

Los ejemplos de estimaciones anteriores se incorporan directamente al prompt del LLM, sin necesidad de bases de datos ni sistemas de recuperación documental.

**Flujo principal:**

Transcripción → FastAPI → Contexto CAG → OpenAI → Estimación JSON

## Inicio rápido

### 1. Instalar dependencias

```powershell
uv sync --frozen
```

### 2. Configurar variables de entorno

```powershell
Copy-Item .env.example .env
```

Añadir la API Key de OpenAI al archivo `.env`.

### 3. Ejecutar

```powershell
uv run uvicorn app.main:app --reload --port 8001
```

### 4. Acceder a Swagger

http://localhost:8001/docs

## Pruebas

Ejecutar los tests automatizados:

```powershell
uv run python -m pytest -v
```

## Documentación

- [Arquitectura del proyecto](docs/architecture.md)
- [Instalación y configuración](docs/setup.md)
- [Documentación de la API](docs/api.md)

### Sesiones del máster

- [Sesión 02 — Scaffolding FastAPI y CAG](docs/sessions/session_02.md)

## Integración continua

El proyecto incorpora un pipeline de GitHub Actions que comprueba la estructura y ejecuta las pruebas automatizadas.

Archivo: `.github/workflows/ci.yml`

## Estado del proyecto

**Sesión 02 — Scaffolding inicial completado localmente.**

- API REST funcional.
- Integración con OpenAI.
- Arquitectura CAG.
- Validación mediante Pydantic.
- Seis pruebas automatizadas superadas.
- Pipeline CI configurado, pendiente de verificar en GitHub.
- Documentación técnica organizada.

## Evolución

Este proyecto evolucionará durante el máster incorporando mejoras en prompt engineering, evaluación de respuestas y nuevas arquitecturas como RAG.
