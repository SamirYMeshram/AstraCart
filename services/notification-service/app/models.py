from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
from sqlalchemy import Boolean, DateTime, Enum as SAEnum, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
class NotificationChannel(str, Enum): EMAIL='EMAIL'; SMS='SMS'; IN_APP='IN_APP'
class NotificationEvent(str, Enum): USER_REGISTERED='USER_REGISTERED'; ORDER_PLACED='ORDER_PLACED'; PAYMENT_SUCCESSFUL='PAYMENT_SUCCESSFUL'; ORDER_SHIPPED='ORDER_SHIPPED'; ORDER_DELIVERED='ORDER_DELIVERED'; REFUND_PROCESSED='REFUND_PROCESSED'
class Notification(Base):
    __tablename__='notifications'
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str]=mapped_column(String(36), index=True)
    channel: Mapped[NotificationChannel]=mapped_column(SAEnum(NotificationChannel), default=NotificationChannel.IN_APP)
    event: Mapped[NotificationEvent]=mapped_column(SAEnum(NotificationEvent), index=True)
    title: Mapped[str]=mapped_column(String(220))
    message: Mapped[str]=mapped_column(Text)
    read: Mapped[bool]=mapped_column(Boolean, default=False, index=True)
    metadata_json: Mapped[dict]=mapped_column(JSON, default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
