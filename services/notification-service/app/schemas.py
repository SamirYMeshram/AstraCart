from datetime import datetime
from pydantic import BaseModel
from app.models import NotificationChannel, NotificationEvent
class NotificationCreate(BaseModel):
    user_id: str
    channel: NotificationChannel = NotificationChannel.IN_APP
    event: NotificationEvent
    title: str
    message: str
    metadata_json: dict = {}
class NotificationOut(BaseModel):
    id: str; user_id: str; channel: NotificationChannel; event: NotificationEvent; title: str; message: str; read: bool; metadata_json: dict; created_at: datetime
    class Config: from_attributes=True
