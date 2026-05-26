from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Notification
from app.schemas import NotificationCreate
class NotificationRepository:
    def __init__(self, db: Session): self.db=db
    def create(self, payload: NotificationCreate) -> Notification:
        n=Notification(**payload.model_dump()); self.db.add(n); self.db.commit(); self.db.refresh(n); return n
    def list(self, user_id: str | None=None, unread: bool | None=None) -> list[Notification]:
        stmt=select(Notification).order_by(Notification.created_at.desc()).limit(100)
        if user_id: stmt=stmt.where(Notification.user_id==user_id)
        if unread is not None: stmt=stmt.where(Notification.read==unread)
        return list(self.db.scalars(stmt))
    def get(self, nid: str) -> Notification | None: return self.db.get(Notification, nid)
    def mark_read(self, n: Notification) -> Notification:
        n.read=True; self.db.commit(); self.db.refresh(n); return n
