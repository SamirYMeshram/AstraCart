from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import uuid4
import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import get_settings

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def create_token(subject: str, role: str, token_type: str = 'access', expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    if expires_delta is None:
        minutes = settings.access_token_expire_minutes if token_type == 'access' else settings.refresh_token_expire_days * 24 * 60
        expires_delta = timedelta(minutes=minutes)
    payload: dict[str, Any] = {
        'sub': subject,
        'role': role,
        'type': token_type,
        'iat': int(now.timestamp()),
        'exp': int((now + expires_delta).timestamp()),
        'jti': str(uuid4()),
        'iss': 'astracart-user-service',
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str, expected_type: str = 'access') -> dict[str, Any]:
    settings = get_settings()
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm], issuer='astracart-user-service')
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired token') from exc
    if payload.get('type') != expected_type:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token type')
    return payload
