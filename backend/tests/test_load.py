import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_concurrent_request_simulation():
    """
    Simulates consecutive rapid requests to model concurrent user load.
    """
    start_time = time.perf_counter()
    iterations = 20
    successful_requests = 0

    for _ in range(iterations):
        response = client.get("/api/v1/health")
        if response.status_code == 200:
            successful_requests += 1

    total_time_ms = (time.perf_counter() - start_time) * 1000
    avg_latency = total_time_ms / iterations

    assert successful_requests == iterations
    # Average latency should remain under 50ms under synthetic local load
    assert avg_latency < 50.0
