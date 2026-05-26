from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
import httpx
from app.core.config import get_settings
from app.core.database import get_db
from app.core.responses import ok
from app.models import PaymentStatus
from app.repositories import PaymentRepository
from app.schemas import PaymentConfirm, PaymentInitiate, PaymentOut
router=APIRouter()
def uid(x_user_id: str | None = Header(default=None)) -> str: return x_user_id or 'demo-customer'
def out(p): return PaymentOut.model_validate(p).model_dump(mode='json')
@router.post('/payments/initiate', status_code=201)
def initiate(payload: PaymentInitiate, user_id: str = Depends(uid), db: Session = Depends(get_db)): return ok('Payment initiated', out(PaymentRepository(db).create(user_id, payload)))
@router.post('/payments/{payment_id}/confirm')
async def confirm(payment_id: str, payload: PaymentConfirm, user_id: str = Depends(uid), db: Session = Depends(get_db)):
    repo=PaymentRepository(db); payment=repo.get(payment_id)
    if not payment: raise HTTPException(status_code=404, detail='Payment not found')
    status=PaymentStatus.FAILED if payload.simulate_failure else PaymentStatus.SUCCESS
    updated=repo.mark(payment, status, {'failure_reason': payload.failure_reason} if payload.simulate_failure else {'processor':'mock_gateway_v2'})
    if status == PaymentStatus.SUCCESS:
        async with httpx.AsyncClient(timeout=5) as client:
            await client.patch(f'{get_settings().order_service_url}/orders/{payment.order_id}/status', json={'status':'PAID','message':'Payment confirmed'}, headers={'X-User-Id': user_id, 'X-User-Role':'ADMIN'})
    return ok('Payment confirmation processed', out(updated))
@router.get('/payments/{payment_id}')
def detail(payment_id: str, db: Session = Depends(get_db)):
    payment=PaymentRepository(db).get(payment_id)
    if not payment: raise HTTPException(status_code=404, detail='Payment not found')
    return ok('Payment retrieved', out(payment))
@router.get('/payments')
def history(user_id: str = Depends(uid), db: Session = Depends(get_db)): return ok('Payment history retrieved', [out(p) for p in PaymentRepository(db).history(user_id)])
@router.post('/payments/{payment_id}/refund')
def refund(payment_id: str, db: Session = Depends(get_db)):
    repo=PaymentRepository(db); payment=repo.get(payment_id)
    if not payment: raise HTTPException(status_code=404, detail='Payment not found')
    if payment.status != PaymentStatus.SUCCESS: raise HTTPException(status_code=409, detail='Only successful payments can be refunded')
    return ok('Payment refunded', out(repo.mark(payment, PaymentStatus.REFUNDED, {'refund_reason':'customer_request'})))
