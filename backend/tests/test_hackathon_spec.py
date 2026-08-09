from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_hackathon_official_interview_spec_flow():
    session_id = "hackathon-spec-sess-001"
    candidate_payload = {
        "member": {
            "id": "CAND-001",
            "name": "Sarah Johnson",
            "jobRole": "Senior Data Engineer",
            "yearsExperience": 9,
            "education": "MS Computer Science",
            "status": "COMPLETED"
        },
        "missions": [
            {"day": 7, "title": "Embeddings Explained", "passed": True, "attempts": 1},
            {"day": 8, "title": "Vector Databases Overview", "passed": True, "attempts": 1}
        ],
        "signals": {"commitDays": 28, "missionsCompleted": 30, "missionsFirstTry": 20}
    }

    # 1. Start Request
    start_resp = client.post(
        "/api/interview",
        json={"sessionId": session_id, "candidate": candidate_payload}
    )
    assert start_resp.status_code == 200
    start_data = start_resp.json()
    assert "reply" in start_data
    assert start_data["done"] is False
    assert "Sarah Johnson" in start_data["reply"]

    # 2. Intermediate Conversation Turns 1 through 7
    for turn in range(7):
        turn_resp = client.post(
            "/api/interview",
            json={"sessionId": session_id, "message": f"Candidate answer for question {turn + 1}"}
        )
        assert turn_resp.status_code == 200
        turn_data = turn_resp.json()
        assert "reply" in turn_data
        assert turn_data["done"] is False

    # 3. Final Turn (Turn 8 -> Completion)
    final_resp = client.post(
        "/api/interview",
        json={"sessionId": session_id, "message": "Final answer for question 8"}
    )
    assert final_resp.status_code == 200
    final_data = final_resp.json()
    assert final_data["done"] is True
    assert "feedback" in final_data
    
    fb = final_data["feedback"]
    assert "summary" in fb
    assert isinstance(fb["strengths"], list)
    assert isinstance(fb["gaps"], list)
    assert isinstance(fb["next"], list)
