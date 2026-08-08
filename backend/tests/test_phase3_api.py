from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_curriculum_endpoint():
    """Tests GET /api/v1/curriculum."""
    response = client.get("/api/v1/curriculum")
    assert response.status_code == 200
    data = response.json()
    assert "curriculum_id" in data
    assert "modules" in data
    assert "days" in data


def test_search_curriculum_topics_endpoint():
    """Tests GET /api/v1/curriculum/search?keyword=fastapi."""
    response = client.get("/api/v1/curriculum/search?keyword=fastapi")
    assert response.status_code == 200
    topics = response.json()
    assert isinstance(topics, list)
    assert len(topics) > 0
    assert any("fastapi" in t["title"].lower() for t in topics)


def test_get_curriculum_day_endpoint():
    """Tests GET /api/v1/curriculum/day/1."""
    response = client.get("/api/v1/curriculum/day/1")
    assert response.status_code == 200
    day = response.json()
    assert day["day_number"] == 1
    assert "topics" in day
    assert "learning_objectives" in day


def test_get_curriculum_day_not_found():
    """Tests GET /api/v1/curriculum/day/999 (404 error)."""
    response = client.get("/api/v1/curriculum/day/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_candidate_endpoint():
    """Tests GET /api/v1/candidate."""
    response = client.get("/api/v1/candidate")
    assert response.status_code == 200
    cand = response.json()
    assert "candidate_id" in cand
    assert "progress" in cand


def test_get_candidate_progress_endpoint():
    """Tests GET /api/v1/candidate/progress."""
    response = client.get("/api/v1/candidate/progress")
    assert response.status_code == 200
    progress = response.json()
    assert "completed_days" in progress
    assert "progress_percentage" in progress


def test_get_candidate_analytics_endpoint():
    """Tests GET /api/v1/candidate/analytics."""
    response = client.get("/api/v1/candidate/analytics")
    assert response.status_code == 200
    analytics = response.json()
    assert "completion_rate" in analytics
    assert "strongest_topics" in analytics
    assert "weakest_topics" in analytics
