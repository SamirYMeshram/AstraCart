from fastapi import Header, HTTPException, status

def actor(x_user_id: str | None = Header(default=None), x_user_role: str | None = Header(default=None)) -> dict[str, str]:
    return {'id': x_user_id or 'system-seller', 'role': x_user_role or 'ADMIN'}

def require_seller_or_admin(actor_data: dict[str, str] = Header(default=None)):
    return actor_data

def ensure_role(role: str | None, allowed: set[str]):
    if role not in allowed:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Insufficient role')
