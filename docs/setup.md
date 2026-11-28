# Instalación y configuración

## 1. Requisitos previos

- Python 3.11 o superior.
- uv como gestor de dependencias.
- Git.
- API Key de OpenAI para llamadas reales.
- Visual Studio Code (recomendado).

### 1.1. Instalar Python

Descargar desde https://www.python.org/downloads/ y comprobar en PowerShell:

```powershell
python --version
```

### 1.2. Instalar uv

En Windows (PowerShell):

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Cerrar y volver a abrir la terminal si es necesario.

```powershell
uv --version
```

Documentación: https://docs.astral.sh/uv/getting-started/installation/

### 1.3. Obtener una API Key de OpenAI

Acceder a https://platform.openai.com/api-keys, iniciar sesión y crear una clave. Guardarla de forma segura. Puede ser necesario configurar la facturación para realizar llamadas reales.

No compartir la clave ni incluirla en el código fuente.

## 2. Clonar el repositorio

```powershell
git clone https://github.com/Mater-AI-Engineering-202611/estimador-cag.git
cd estimador-cag
```

Comprobar que la URL corresponde al repositorio publicado. Si los cambios Multi-turn todavía están en una rama de desarrollo, seleccionar esa rama antes de instalar las dependencias.

## 3. Instalar dependencias

```powershell
uv sync --locked --dev
```

El comando instala las dependencias de `pyproject.toml` utilizando `uv.lock`, comprueba que el lockfile está actualizado y crea `.venv` si es necesario.

Si todavía no se ha incorporado pytest-asyncio durante el desarrollo de la rama:

```powershell
uv add --dev pytest-asyncio
```

Versionar los cambios de `pyproject.toml` y `uv.lock`. Una vez actualizados, no es necesario volver a añadir la dependencia al clonar el proyecto.

## 4. Configurar variables de entorno

Crear `.env` a partir de la plantilla si todavía no existe:

```powershell
Copy-Item .env.example .env
```

Configurar:

```dotenv
OPENAI_API_KEY=tu_api_key
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
APP_ENV=development
```

Sustituir `tu_api_key` por la clave real. `.env` debe estar excluido del control de versiones mediante `.gitignore`.

No se necesitan variables adicionales para Multi-turn.

## 5. Ejecutar la aplicación

```powershell
uv run uvicorn app.main:app --reload --port 8001
```

La API estará disponible en http://localhost:8001.

`--reload` reinicia el proceso al detectar cambios de código. Esto implica perder las conversaciones almacenadas en RAM.

Si el puerto está ocupado, se puede utilizar otro:

```powershell
uv run uvicorn app.main:app --reload --port 8002
```

Adaptar las URLs al puerto elegido. Para detener el servidor, pulsar `Ctrl + C`.

## 6. Comprobar el funcionamiento

### Health Check

Abrir http://localhost:8001/health.

```json
{"status": "healthy"}
```

### Swagger

Abrir http://localhost:8001/docs.

- Single-turn: probar `POST /api/v1/estimate` con una transcripción.
- Multi-turn: probar `POST /api/v1/conversation/estimate` sin identificador y copiar el `conversation_id` devuelto. Enviar una segunda petición con ese identificador y un refinamiento.

Las llamadas reales requieren una API Key válida y pueden generar costes.

## 7. Ejecutar pruebas automatizadas

```powershell
uv run python -m pytest -v
```

La suite actual contiene 42 casos previstos, incluidos los parametrizados. Comprueba el contexto CAG, historial, aislamiento, Sliding Window, servicio LLM, endpoints y health check.

Los tests utilizan mocks y no necesitan una API Key real ni consumen tokens de OpenAI.

## 8. Comprobar calidad del código

```powershell
uv run ruff check .
uv run ruff format --check .
```

El primer comando realiza análisis estático; el segundo comprueba el formato sin modificar los ficheros.

## 9. Integración continua

El workflow existente se encuentra en `.github/workflows/ci.yml`. Está previsto para eventos `push` y `pull_request`.

Comprobar que sincroniza las dependencias de desarrollo, incluyendo pytest-asyncio, y ejecuta la suite de pruebas. La validación del workflow actualizado queda pendiente de confirmar.

## 10. Resumen de comandos

| Acción | Comando |
|---|---|
| Comprobar Python | `python --version` |
| Comprobar uv | `uv --version` |
| Instalar dependencias | `uv sync --locked --dev` |
| Crear `.env` | `Copy-Item .env.example .env` |
| Arrancar API | `uv run uvicorn app.main:app --reload --port 8001` |
| Ejecutar tests | `uv run python -m pytest -v` |
| Comprobar código | `uv run ruff check .` |
| Comprobar formato | `uv run ruff format --check .` |

URLs principales:

- API: http://localhost:8001
- Health Check: http://localhost:8001/health
- Swagger: http://localhost:8001/docs
