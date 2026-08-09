from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "curriculumLoaded" in data
    assert "candidateLoaded" in data


def test_health_v1_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ["running", "ok", "healthy"]


def test_curriculum_endpoint():
    response = client.get("/api/v1/curriculum")
    assert response.status_code == 200
    data = response.json()
    assert "curriculum_id" in data


def test_candidate_endpoint():
    response = client.get("/api/v1/candidate")
    assert response.status_code == 200
    data = response.json()
    assert "candidate_id" in data
