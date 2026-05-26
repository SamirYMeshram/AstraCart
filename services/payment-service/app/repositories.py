from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Payment, PaymentStatus
from app.schemas import PaymentInitiate
class PaymentRepository:
    def __init__(self, db: Session): self.db=db
    def create(self, user_id: str, payload: PaymentInitiate) -> Payment:
        payment=Payment(user_id=user_id, order_id=payload.order_id, amount=payload.amount, currency=payload.currency, method=payload.method, gateway_reference=f'ASTRA-PAY-{uuid4().hex[:12].upper()}')
        self.db.add(payment); self.db.commit(); self.db.refresh(payment); return payment
    def get(self, payment_id: str) -> Payment | None: return self.db.get(Payment, payment_id)
    def history(self, user_id: str | None=None) -> list[Payment]:
        stmt=select(Payment).order_by(Payment.created_at.desc()).limit(100)
        if user_id: stmt=stmt.where(Payment.user_id==user_id)
        return list(self.db.scalars(stmt))
    def mark(self, payment: Payment, status: PaymentStatus, metadata: dict | None=None) -> Payment:
        payment.status=status
        if metadata: payment.metadata_json={**(payment.metadata_json or {}), **metadata}
        if status == PaymentStatus.SUCCESS: payment.receipt=f'Receipt {payment.gateway_reference}: paid {payment.currency} {payment.amount:.2f} for order {payment.order_id}'
        if status == PaymentStatus.REFUNDED: payment.receipt=f'Refund receipt {payment.gateway_reference}: refunded {payment.currency} {payment.amount:.2f}'
        self.db.commit(); self.db.refresh(payment); return payment
