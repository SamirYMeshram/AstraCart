from datetime import datetime
from pydantic import BaseModel, Field
from app.models import OrderStatus
class OrderCreate(BaseModel):
    shipping_address: dict = Field(default_factory=dict)
    customer_email: str | None = None
class StatusUpdate(BaseModel):
    status: OrderStatus
    message: str | None = None
class OrderItemOut(BaseModel):
    id: str; product_id: str; title: str; unit_price: float; quantity: int; line_total: float
    class Config: from_attributes=True
class TimelineOut(BaseModel):
    id: str; status: OrderStatus; message: str; actor_id: str | None; created_at: datetime
    class Config: from_attributes=True
class OrderOut(BaseModel):
    id: str; user_id: str; customer_email: str | None; status: OrderStatus; subtotal: float; tax: float; shipping_fee: float; total: float; shipping_address: dict; created_at: datetime; updated_at: datetime
    items: list[OrderItemOut] = []
    timeline: list[TimelineOut] = []
    class Config: from_attributes=True
