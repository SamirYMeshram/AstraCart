from __future__ import annotations
import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import create_token, decode_token, verify_password
from app.repositories import UserRepository
from app.schemas import LoginRequest, RefreshRequest, TokenPair, UserCreate, UserOut

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.users = UserRepository(db)

    def register(self, payload: UserCreate) -> TokenPair:
        if self.users.by_email(payload.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already registered')
        user = self.users.create(payload)
        return self._issue(user)

    def login(self, payload: LoginRequest) -> TokenPair:
        user = self.users.by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Account disabled')
        return self._issue(user)

    def refresh(self, payload: RefreshRequest) -> TokenPair:
        decoded = decode_token(payload.refresh_token, expected_type='refresh')
        user = self.users.by_id(decoded['sub'])
        if not user or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Refresh token subject not found')
        return self._issue(user)

    def _issue(self, user) -> TokenPair:
        access = create_token(user.id, user.role.value, 'access')
        refresh = create_token(user.id, user.role.value, 'refresh')
        return TokenPair(access_token=access, refresh_token=refresh, user=UserOut.model_validate(user))
