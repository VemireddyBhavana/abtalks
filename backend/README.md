# AI Interview Agent - FastAPI Backend

Production-ready Python FastAPI backend foundation for the ABTalks AI Interview Agent project.

## Architecture

- **`app/main.py`**: FastAPI application entry point, CORS middleware setup, router inclusion, and root health check endpoint.
- **`app/api/`**: API routes and controllers.
- **`app/core/`**: Configuration management (`config.py`) using Pydantic Settings and logging setup (`logging_config.py`).
- **`app/models/`**: Pydantic data schemas for request validation and response models.
- **`app/services/`**: Business logic layer.
- **`app/utils/`**: Helper utilities and shared functions.
- **`app/data/`**: Static datasets or local data stores.

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run development server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

3. Interactive Docs:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`
