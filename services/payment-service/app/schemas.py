from datetime import datetime
from pydantic import BaseModel, Field
from app.models import PaymentStatus
class PaymentInitiate(BaseModel):
    order_id: str
    amount: float = Field(gt=0)
    currency: str = 'INR'
    method: str = 'mock_card'
class PaymentConfirm(BaseModel):
    simulate_failure: bool = False
    failure_reason: str | None = None
class PaymentOut(BaseModel):
    id: str; order_id: str; user_id: str; amount: float; currency: str; gateway_reference: str; status: PaymentStatus; method: str; receipt: str | None; metadata_json: dict; created_at: datetime; updated_at: datetime
    class Config: from_attributes=True
