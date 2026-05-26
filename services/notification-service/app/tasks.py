from celery import Celery
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.repositories import NotificationRepository
from app.schemas import NotificationCreate
settings=get_settings(); celery_app=Celery('notification_tasks', broker=settings.celery_broker_url, backend=settings.celery_result_backend)
@celery_app.task(name='app.tasks.dispatch_notification')
def dispatch_notification(payload: dict):
    db=SessionLocal()
    try:
        n=NotificationRepository(db).create(NotificationCreate(**payload))
        return {'notification_id': n.id, 'channel': n.channel.value, 'delivered': True}
    finally: db.close()
@celery_app.task(name='app.tasks.generate_daily_sales_report')
def generate_daily_sales_report(): return {'report':'daily-sales','status':'generated','format':'mock-pdf'}
