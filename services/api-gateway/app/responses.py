from typing import Any
def ok(message: str, data: Any=None): return {'success': True, 'message': message, 'data': data if data is not None else {}}
def fail(message: str, error: str): return {'success': False, 'message': message, 'error': error}
