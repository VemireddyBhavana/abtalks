import json
from typing import Any, Dict
from app.utils.file_utils import ensure_file_exists


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Utility to load and parse JSON content from disk.
    Raises FileNotFoundError if file is missing, or json.JSONDecodeError if malformed.
    """
    abs_path = ensure_file_exists(file_path)
    with open(abs_path, "r", encoding="utf-8") as f:
        return json.load(f)
