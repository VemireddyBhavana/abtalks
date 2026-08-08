import uuid
from datetime import datetime, timezone


def generate_unique_id(prefix: str = "session") -> str:
    """
    Utility function to generate a unique ID string.
    """
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def get_utc_now() -> str:
    """
    Utility function to get current ISO formatted UTC timestamp.
    """
    return datetime.now(timezone.utc).isoformat()
