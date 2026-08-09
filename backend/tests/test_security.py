from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_security_headers_present():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert "Strict-Transport-Security" in response.headers
    assert "X-Process-Time" in response.headers


def test_request_payload_size_limit():
    large_payload = "x" * (2 * 1024 * 1024 + 100)
    response = client.post("/api/v1/interview/submit", headers={"Content-Length": str(len(large_payload))})
    assert response.status_code == 413
    assert "Payload too large" in response.json()["detail"]
