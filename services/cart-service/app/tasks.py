from celery import Celery
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.repositories import CartRepository
settings=get_settings()
celery_app=Celery('cart_tasks', broker=settings.celery_broker_url, backend=settings.celery_result_backend)
celery_app.conf.beat_schedule={'clean-expired-carts': {'task':'app.tasks.clean_expired_carts','schedule':3600.0}}
@celery_app.task(name='app.tasks.clean_expired_carts')
def clean_expired_carts():
    db=SessionLocal()
    try: return {'deleted': CartRepository(db).cleanup_expired()}
    finally: db.close()
