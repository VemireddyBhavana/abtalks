import json
import pytest
from app.services.candidate_service import CandidateService
from app.exceptions.candidate_exception import (
    CandidateNotFoundError,
    CandidateValidationError,
)


def test_candidate_analytics_and_methods(tmp_path):
    """Verifies candidate analytics methods: completion rate, completed/remaining days, strongest/weakest topics."""
    candidate_file = tmp_path / "test_candidate.json"
    dummy_data = {
        "candidate_id": "cand_1",
        "full_name": "Test Candidate",
        "email": "test@example.com",
        "target_role": "AI Engineer",
        "experience_level": "Senior",
        "progress": {
            "completed_days": [1, 2],
            "incomplete_days": [3, 4],
            "total_days": 4,
            "progress_percentage": 50.0
        },
        "completed_topics": ["top_1", "top_2"],
        "skipped_topics": [],
        "learning_signals": [
            {"category": "Strength", "signal": "Good comprehension of FastAPI", "score": 95},
            {"category": "Area for Growth", "signal": "Needs practice with context buffers", "score": 60}
        ],
        "recent_activity": [
            {"day_number": 2, "activity_type": "Assessment Done", "timestamp": "2026-08-08T00:00:00Z"}
        ]
    }
    candidate_file.write_text(json.dumps(dummy_data), encoding="utf-8")

    service = CandidateService(data_path=str(candidate_file))

    # Analytics checks
    assert service.get_completion_rate() == 0.5
    assert service.get_total_completed_days() == 2
    assert service.get_total_remaining_days() == 2

    strongest = service.get_strongest_topics()
    assert len(strongest) == 1
    assert strongest[0].score == 95

    weakest = service.get_weakest_topics()
    assert len(weakest) == 1
    assert weakest[0].score == 60

    # Cache refresh check
    refreshed = service.refresh_cache()
    assert refreshed.candidate_id == "cand_1"

    # Restore default candidate cache after test
    CandidateService().refresh_cache()


def test_candidate_missing_file_custom_exception():
    """Verifies missing file raises CandidateNotFoundError."""
    with pytest.raises(CandidateNotFoundError):
        CandidateService(data_path="/non_existent_path/candidate.json")


def test_candidate_invalid_json_custom_exception(tmp_path):
    """Verifies malformed JSON raises CandidateValidationError."""
    bad_file = tmp_path / "bad_candidate.json"
    bad_file.write_text("{ malformed }", encoding="utf-8")

    with pytest.raises(CandidateValidationError, match="corrupted"):
        CandidateService(data_path=str(bad_file))
