import json
import pytest
from app.services.curriculum_service import CurriculumService
from app.exceptions.curriculum_exception import (
    CurriculumNotFoundError,
    CurriculumValidationError,
)


def test_curriculum_loading_search_and_caching(tmp_path):
    """Verifies search_topic, search_learning_objective, search_tool, and get_days_using_tool."""
    curriculum_file = tmp_path / "test_curriculum.json"
    dummy_data = {
        "curriculum_id": "test_curr",
        "title": "Test Curriculum Title",
        "version": "1.0.0",
        "modules": [
            {"id": "m1", "title": "Module One", "description": "Desc M1"}
        ],
        "days": [
          {
            "day_number": 1,
            "module_id": "m1",
            "title": "Day One",
            "description": "Desc D1",
            "topics": [
              {"id": "top_fastapi", "title": "FastAPI Core", "category": "Backend"},
              {"id": "top_react", "title": "React Architecture", "category": "Frontend"}
            ],
            "learning_objectives": ["Build FastAPI Microservices", "Master React Router"],
            "tools_used": ["FastAPI", "React", "Docker"]
          }
        ]
    }
    curriculum_file.write_text(json.dumps(dummy_data), encoding="utf-8")

    service = CurriculumService(data_path=str(curriculum_file))

    # Search topic
    fastapi_topics = service.search_topic("fastapi")
    assert len(fastapi_topics) == 1
    assert fastapi_topics[0].id == "top_fastapi"

    # Search learning objective
    objectives = service.search_learning_objective("microservices")
    assert len(objectives) == 1
    assert "FastAPI" in objectives[0]

    # Search tool & days using tool
    tools = service.search_tool("dock")
    assert tools == ["Docker"]
    days = service.get_days_using_tool("FastAPI")
    assert len(days) == 1
    assert days[0].day_number == 1

    # Refresh cache
    refreshed = service.refresh_cache()
    assert refreshed.curriculum_id == "test_curr"

    # Restore default curriculum cache after test
    CurriculumService().refresh_cache()


def test_curriculum_missing_file_custom_exception():
    """Verifies that missing curriculum file raises CurriculumNotFoundError."""
    with pytest.raises(CurriculumNotFoundError):
        CurriculumService(data_path="/non_existent_path/curriculum.json")


def test_curriculum_invalid_json_custom_exception(tmp_path):
    """Verifies that corrupted JSON raises CurriculumValidationError."""
    invalid_file = tmp_path / "bad.json"
    invalid_file.write_text("{ invalid json }", encoding="utf-8")

    with pytest.raises(CurriculumValidationError, match="corrupted"):
        CurriculumService(data_path=str(invalid_file))


def test_curriculum_schema_validation_failure_custom_exception(tmp_path):
    """Verifies that invalid schema raises CurriculumValidationError."""
    bad_schema_file = tmp_path / "bad_schema.json"
    bad_schema_file.write_text(json.dumps({"title": "Missing Required Fields"}), encoding="utf-8")

    with pytest.raises(CurriculumValidationError, match="validation failed"):
        CurriculumService(data_path=str(bad_schema_file))
