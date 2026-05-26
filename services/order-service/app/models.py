from __future__ import annotations
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4
from sqlalchemy import DateTime, Enum as SAEnum, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
class OrderStatus(str, Enum):
    PENDING='PENDING'; CONFIRMED='CONFIRMED'; PAID='PAID'; PACKED='PACKED'; SHIPPED='SHIPPED'; OUT_FOR_DELIVERY='OUT_FOR_DELIVERY'; DELIVERED='DELIVERED'; CANCELLED='CANCELLED'; REFUNDED='REFUNDED'
class Order(Base):
    __tablename__='orders'
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str]=mapped_column(String(36), index=True, nullable=False)
    customer_email: Mapped[str | None]=mapped_column(String(255))
    status: Mapped[OrderStatus]=mapped_column(SAEnum(OrderStatus), default=OrderStatus.PENDING, index=True)
    subtotal: Mapped[float]=mapped_column(Float, nullable=False)
    tax: Mapped[float]=mapped_column(Float, default=0)
    shipping_fee: Mapped[float]=mapped_column(Float, default=0)
    total: Mapped[float]=mapped_column(Float, nullable=False)
    shipping_address: Mapped[dict]=mapped_column(JSON, default=dict)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    items: Mapped[list['OrderItem']]=relationship(back_populates='order', cascade='all, delete-orphan')
    timeline: Mapped[list['OrderTimeline']]=relationship(back_populates='order', cascade='all, delete-orphan')
class OrderItem(Base):
    __tablename__='order_items'
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    order_id: Mapped[str]=mapped_column(ForeignKey('orders.id'), index=True)
    product_id: Mapped[str]=mapped_column(String(36), index=True)
    title: Mapped[str]=mapped_column(String(220))
    unit_price: Mapped[float]=mapped_column(Float)
    quantity: Mapped[int]=mapped_column(Integer)
    line_total: Mapped[float]=mapped_column(Float)
    order: Mapped[Order]=relationship(back_populates='items')
class OrderTimeline(Base):
    __tablename__='order_timeline'
    id: Mapped[str]=mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    order_id: Mapped[str]=mapped_column(ForeignKey('orders.id'), index=True)
    status: Mapped[OrderStatus]=mapped_column(SAEnum(OrderStatus))
    message: Mapped[str]=mapped_column(Text)
    actor_id: Mapped[str | None]=mapped_column(String(36))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    order: Mapped[Order]=relationship(back_populates='timeline')
