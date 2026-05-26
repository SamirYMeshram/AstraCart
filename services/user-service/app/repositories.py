from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Role, User
from app.core.security import hash_password
from app.schemas import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def by_email(self, email: str) -> User | None:
        return self.db.scalar(select(User).where(User.email == email.lower()))

    def by_id(self, user_id: str) -> User | None:
        return self.db.get(User, user_id)

    def create(self, payload: UserCreate) -> User:
        user = User(email=payload.email.lower(), full_name=payload.full_name, role=payload.role, password_hash=hash_password(payload.password))
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, payload: UserUpdate) -> User:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_users(self, role: Role | None = None, limit: int = 100) -> list[User]:
        stmt = select(User).order_by(User.created_at.desc()).limit(limit)
        if role:
            stmt = stmt.where(User.role == role)
        return list(self.db.scalars(stmt))

    def set_role(self, user: User, role: Role) -> User:
        user.role = role
        self.db.commit()
        self.db.refresh(user)
        return user
