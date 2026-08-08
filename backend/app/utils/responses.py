from typing import Any, Optional
from fastapi.responses import JSONResponse


def success_response(data: Any, message: str = "Success", status_code: int = 200) -> JSONResponse:
    """
    Standardized API success response helper wrapper.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data,
        },
    )


def error_response(message: str, error_code: Optional[str] = None, status_code: int = 400) -> JSONResponse:
    """
    Standardized API error response helper wrapper.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "error_code": error_code or "BAD_REQUEST",
        },
    )
