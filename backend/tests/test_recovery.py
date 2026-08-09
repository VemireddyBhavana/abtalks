import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_session_recovery_after_interruption():
    """
    Tests session state recovery via GET /api/v1/interview/{session_id} after interruption.
    """
    # 1. Start session
    start_resp = client.post("/api/v1/interview/start", json={"candidate_id": "cand_recovery_test"})
    assert start_resp.status_code == 200
    session_id = start_resp.json()["session_id"]

    # 2. Answer turn 1
    ans_resp = client.post(
        "/api/v1/interview/answer",
        json={"session_id": session_id, "answer_text": "Detailed technical answer for turn 1."}
    )
    assert ans_resp.status_code == 200

    # 3. Simulate page refresh / reconnect: recover state
    recovered_state = client.get(f"/api/v1/interview/{session_id}")
    assert recovered_state.status_code == 200
    data = recovered_state.json()
    assert data["session_id"] == session_id
    assert data["current_question_index"] == 1


def test_invalid_session_id_recovery_failure():
    """
    Tests 404 response when attempting to recover state for non-existent session ID.
    """
    resp = client.get("/api/v1/interview/non_existent_session_99999")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"].lower()
