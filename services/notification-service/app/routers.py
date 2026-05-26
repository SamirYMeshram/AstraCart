from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.responses import ok
from app.repositories import NotificationRepository
from app.schemas import NotificationCreate, NotificationOut
router=APIRouter()
def uid(x_user_id: str | None = Header(default=None)) -> str: return x_user_id or 'demo-customer'
def out(n): return NotificationOut.model_validate(n).model_dump(mode='json')
@router.post('/notifications', status_code=201)
def create(payload: NotificationCreate, db: Session = Depends(get_db)): return ok('Notification created', out(NotificationRepository(db).create(payload)))
@router.get('/notifications')
def notifications(unread: bool | None = Query(default=None), user_id: str = Depends(uid), db: Session = Depends(get_db)): return ok('Notifications retrieved', [out(n) for n in NotificationRepository(db).list(user_id, unread)])
@router.patch('/notifications/{notification_id}/read')
def read(notification_id: str, db: Session = Depends(get_db)):
    repo=NotificationRepository(db); n=repo.get(notification_id)
    if not n: raise HTTPException(status_code=404, detail='Notification not found')
    return ok('Notification marked as read', out(repo.mark_read(n)))
