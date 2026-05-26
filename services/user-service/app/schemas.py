from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from app.models import Role

class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=160)
    password: str = Field(min_length=8, max_length=128)
    role: Role = Role.CUSTOMER

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class UserUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=160)
    phone: str | None = None
    avatar_url: str | None = None

class RoleUpdate(BaseModel):
    role: Role

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    role: Role
    phone: str | None = None
    avatar_url: str | None = None
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'
    user: UserOut
