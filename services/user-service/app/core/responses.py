from __future__ import annotations
from typing import Any

def ok(message: str, data: Any = None) -> dict[str, Any]:
    return {'success': True, 'message': message, 'data': data if data is not None else {}}

def fail(message: str, error: str) -> dict[str, Any]:
    return {'success': False, 'message': message, 'error': error}
