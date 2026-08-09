from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_full_interview_session_flow():
    # 1. Start interview session
    start_resp = client.post("/api/v1/interview/start", json={"candidate_id": "cand_alex_dev_99"})
    assert start_resp.status_code == 200
    start_data = start_resp.json()
    assert "session_id" in start_data
    session_id = start_data["session_id"]

    # 2. Get current state
    state_resp = client.get(f"/api/v1/interview/{session_id}")
    assert state_resp.status_code == 200
    state_data = state_resp.json()
    assert state_data["session_id"] == session_id

    # 3. Submit turn answer
    submit_resp = client.post(
        "/api/v1/interview/answer",
        json={"session_id": session_id, "answer_text": "I implement comprehensive error boundaries and use memoization hooks for optimal rendering performance."}
    )
    assert submit_resp.status_code == 200
    submit_data = submit_resp.json()
    assert submit_data["session_id"] == session_id
    assert "done" in submit_data
