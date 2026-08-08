import json
from typing import Dict, Any
from app.memory.memory_models import InterviewMemory


class MemorySerializer:
    """
    Normalizes and serializes/deserializes InterviewMemory objects to/from JSON dict payloads.
    """

    @classmethod
    def serialize(cls, memory: InterviewMemory) -> Dict[str, Any]:
        """Serializes InterviewMemory model instance to JSON dictionary payload."""
        return memory.model_dump()

    @classmethod
    def deserialize(cls, payload: Dict[str, Any]) -> InterviewMemory:
        """Deserializes JSON dictionary payload into an InterviewMemory model instance."""
        return InterviewMemory.model_validate(payload)

    @classmethod
    def to_json_string(cls, memory: InterviewMemory) -> str:
        """Converts InterviewMemory to pretty JSON string."""
        return json.dumps(cls.serialize(memory), indent=2)
