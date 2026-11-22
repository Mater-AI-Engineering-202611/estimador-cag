# Instalación y configuración

## 1. Requisitos previos

Para ejecutar el proyecto necesitamos:

- Python 3.11 o superior.
- uv como gestor de dependencias.
- Git.
- Una API Key de OpenAI.
- Visual Studio Code (recomendado).

### 1.1. Instalar Python

Descargar Python desde:

https://www.python.org/downloads/

Comprobar la instalación desde PowerShell:

```powershell
python --version
```

El proyecto utiliza Python 3.11.

### 1.2. Instalar uv

`uv` es el gestor de dependencias y entornos virtuales utilizado en este proyecto.

**Instalación en Windows (PowerShell):**

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Una vez instalado, cerrar y volver a abrir PowerShell si fuera necesario.

Comprobar la instalación:

```powershell
uv --version
```

Documentación oficial:

https://docs.astral.sh/uv/getting-started/installation/

### 1.3. Obtener una API Key de OpenAI

Para utilizar el modelo de inteligencia artificial necesitamos una API Key de OpenAI.

**Pasos:**

1. Acceder a https://platform.openai.com/
2. Iniciar sesión o crear una cuenta.
3. Acceder a https://platform.openai.com/api-keys
4. Seleccionar **Create new secret key**.
5. Crear la clave y copiarla.
6. Guardarla de forma segura para configurarla posteriormente en el archivo `.env`.

**Importante:**

- La API Key es privada y no debe compartirse.
- No debe incluirse en el código fuente ni subirse a GitHub.
- El uso de la API puede generar costes según el modelo y las peticiones realizadas.
- Puede ser necesario configurar la facturación en OpenAI Platform.

## 2. Clonar el repositorio

Desde PowerShell, ejecutar:

```powershell
git clone https://github.com/Mater-AI-Engineering-202611/estimador-cag.git
cd estimador-cag
```

**Nota:** verificar que la URL corresponde al repositorio publicado en GitHub.

## 3. Instalar dependencias

Desde la raíz del proyecto:

```powershell
uv sync --frozen
```

Este comando instala las dependencias definidas en `pyproject.toml`, utilizando las versiones de `uv.lock`.

También crea el entorno virtual `.venv` si no existe.

## 4. Configurar variables de entorno

Crear un archivo `.env` a partir de `.env.example`:

```powershell
Copy-Item .env.example .env
```

Abrir el archivo `.env` y configurar las variables:

```dotenv
OPENAI_API_KEY=tu_api_key
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
```

Sustituir `tu_api_key` por la clave obtenida desde OpenAI Platform.

**Importante:** nunca subir `.env` al repositorio. Este archivo debe estar incluido en `.gitignore`.

## 5. Ejecutar la aplicación

Desde la raíz del proyecto:

```powershell
uv run uvicorn app.main:app --reload --port 8001
```

La API estará disponible en:

http://localhost:8001

El parámetro `--reload` reinicia automáticamente el servidor cuando detecta cambios en el código.

Si el puerto `8001` está ocupado, podemos utilizar otro:

```powershell
uv run uvicorn app.main:app --reload --port 8002
```

En ese caso, también debemos cambiar el puerto en las URLs utilizadas para acceder a la aplicación.

Para detener el servidor, pulsar `Ctrl + C` en la terminal.

## 6. Comprobar el funcionamiento

### Health Check

Abrir:

http://localhost:8001/health

Respuesta esperada:

```json
{
  "status": "healthy"
}
```

### Documentación Swagger

Abrir:

http://localhost:8001/docs

Desde Swagger podemos probar el endpoint:

`POST /api/v1/estimate`

Para generar una estimación real, es necesario haber configurado correctamente la API Key de OpenAI.

## 7. Ejecutar pruebas automatizadas

```powershell
uv run python -m pytest -v
```

Los tests comprueban:

- Funcionamiento del endpoint de salud.
- Validación de transcripciones.
- Generación de estimaciones mediante mocks.
- Existencia de ejemplos CAG.
- Construcción del system prompt.

Las pruebas automatizadas utilizan mocks y no necesitan consumir créditos de OpenAI.

## 8. Comprobar calidad del código

```powershell
uv run ruff check .
```

Este comando analiza el código para detectar posibles problemas de calidad y estilo.

## 9. Integración continua

El repositorio dispone de un workflow de GitHub Actions.

Cuando se realiza un `push` o se abre un Pull Request, se ejecutan automáticamente:

- Instalación de dependencias.
- Verificación de la estructura del proyecto.
- Ejecución de tests.

El workflow se encuentra en:

`.github/workflows/ci.yml`

**Nota:** comprobar que la carpeta se llama `workflows` (en plural), ya que GitHub Actions requiere esa ubicación.

## 10. Resumen de comandos

| Acción | Comando |
|---|---|
| Comprobar Python | `python --version` |
| Comprobar uv | `uv --version` |
| Instalar dependencias | `uv sync --frozen` |
| Crear `.env` | `Copy-Item .env.example .env` |
| Arrancar API | `uv run uvicorn app.main:app --reload --port 8001` |
| Ejecutar tests | `uv run python -m pytest -v` |
| Comprobar código | `uv run ruff check .` |

**URLs principales:**

- API: http://localhost:8001
- Health Check: http://localhost:8001/health
- Swagger: http://localhost:8001/docs
