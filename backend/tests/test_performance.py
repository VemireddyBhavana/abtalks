import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint_response_time():
    start = time.perf_counter()
    response = client.get("/api/v1/health")
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert response.status_code == 200
    # Health endpoint should respond in under 100ms
    assert elapsed_ms < 100.0


def test_root_endpoint_response_time():
    start = time.perf_counter()
    response = client.get("/")
    elapsed_ms = (time.perf_counter() - start) * 1000
    assert response.status_code == 200
    assert elapsed_ms < 100.0
