import os


def ensure_file_exists(file_path: str) -> str:
    """
    Ensures that a file exists at file_path (resolving relative paths against current workspace).
    Returns absolute path if file exists, else raises FileNotFoundError.
    """
    if os.path.isabs(file_path):
        abs_path = file_path
    else:
        # Try resolving relative path against backend root directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        abs_path = os.path.join(base_dir, file_path)

    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"File not found at resolved path: '{abs_path}'")

    return abs_path
