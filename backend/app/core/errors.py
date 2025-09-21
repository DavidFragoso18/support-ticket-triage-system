import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

def internal_error(code: str, msg: str, *, extra: dict | None = None) -> HTTPException:
    # Keep details minimal; don’t leak internals
    payload = {"code": code, "message": msg}
    if extra:
        payload["details"] = extra
    return HTTPException(status_code=500, detail=payload)

def not_found(code: str, msg: str) -> HTTPException:
    return HTTPException(status_code=404, detail={"code": code, "message": msg})
