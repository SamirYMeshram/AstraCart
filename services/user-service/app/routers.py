from __future__ import annotations
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.responses import ok
from app.dependencies import current_user, require_roles
from app.models import Role, User
from app.repositories import UserRepository
from app.schemas import LoginRequest, RefreshRequest, RoleUpdate, UserCreate, UserOut, UserUpdate
from app.services import AuthService

router = APIRouter()

@router.post('/auth/register', status_code=201)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    return ok('User registered successfully', AuthService(db).register(payload).model_dump(mode='json'))

@router.post('/auth/login')
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return ok('Login successful', AuthService(db).login(payload).model_dump(mode='json'))

@router.post('/auth/refresh')
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    return ok('Token refreshed', AuthService(db).refresh(payload).model_dump(mode='json'))

@router.get('/users/me')
def me(user: User = Depends(current_user)):
    return ok('Current user profile', UserOut.model_validate(user).model_dump(mode='json'))

@router.patch('/users/me')
def update_me(payload: UserUpdate, user: User = Depends(current_user), db: Session = Depends(get_db)):
    updated = UserRepository(db).update(user, payload)
    return ok('Profile updated', UserOut.model_validate(updated).model_dump(mode='json'))

@router.get('/admin/users')
def admin_users(role: Role | None = Query(default=None), db: Session = Depends(get_db), _: User = Depends(require_roles(Role.ADMIN, Role.SUPPORT))):
    users = UserRepository(db).list_users(role=role)
    return ok('Users retrieved', [UserOut.model_validate(u).model_dump(mode='json') for u in users])

@router.patch('/admin/users/{user_id}/role')
def admin_role_update(user_id: str, payload: RoleUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(Role.ADMIN))):
    repo = UserRepository(db)
    target = repo.by_id(user_id)
    if not target:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail='User not found')
    return ok('User role updated', UserOut.model_validate(repo.set_role(target, payload.role)).model_dump(mode='json'))
