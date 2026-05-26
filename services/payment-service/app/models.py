from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
from sqlalchemy import DateTime, Enum as SAEnum, Float, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
class PaymentStatus(str, Enum): INITIATED='INITIATED'; SUCCESS='SUCCESS'; FAILED='FAILED'; REFUNDED='REFUNDED'
class Payment(Base):
    __tablename__='payments'
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    order_id: Mapped[str]=mapped_column(String(36), index=True, nullable=False)
    user_id: Mapped[str]=mapped_column(String(36), index=True, nullable=False)
    amount: Mapped[float]=mapped_column(Float, nullable=False)
    currency: Mapped[str]=mapped_column(String(8), default='INR')
    gateway_reference: Mapped[str]=mapped_column(String(80), unique=True, index=True)
    status: Mapped[PaymentStatus]=mapped_column(SAEnum(PaymentStatus), default=PaymentStatus.INITIATED, index=True)
    method: Mapped[str]=mapped_column(String(40), default='mock_card')
    receipt: Mapped[str | None]=mapped_column(Text)
    metadata_json: Mapped[dict]=mapped_column(JSON, default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
