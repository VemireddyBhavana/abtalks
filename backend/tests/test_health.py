import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_health_check_diagnostics():
    """
    Test root health check endpoint GET /
    Should return status 'running', project title, and readiness flags for curriculum, candidate, and cache.
    """
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["project"] == "AI Interview Agent"
    assert data["curriculumLoaded"] is True
    assert data["candidateLoaded"] is True
    assert data["cacheReady"] is True


def test_v1_health_check_diagnostics():
    """
    Test API v1 health check endpoint GET /api/v1/health
    Should return healthy status response with cache readiness metadata.
    """
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["curriculumLoaded"] is True
    assert data["candidateLoaded"] is True
    assert data["cacheReady"] is True
