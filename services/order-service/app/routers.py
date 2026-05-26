from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.responses import ok
from app.models import OrderStatus
from app.repositories import OrderRepository
from app.schemas import OrderCreate, OrderOut, StatusUpdate
from app.services import OrderService
router=APIRouter()
def uid(x_user_id: str | None = Header(default=None)) -> str: return x_user_id or 'demo-customer'
def role(x_user_role: str | None = Header(default=None)) -> str: return x_user_role or 'CUSTOMER'
def out(o): return OrderOut.model_validate(o).model_dump(mode='json')
@router.post('/orders', status_code=201)
async def create_order(payload: OrderCreate, user_id: str = Depends(uid), db: Session = Depends(get_db)): return ok('Order created from cart', out(await OrderService(OrderRepository(db)).create_from_cart(user_id, payload)))
@router.get('/orders')
def orders(user_id: str = Depends(uid), actor_role: str = Depends(role), db: Session = Depends(get_db)):
    return ok('Orders retrieved', [out(o) for o in OrderRepository(db).list(None if actor_role in {'ADMIN','SUPPORT'} else user_id)])
@router.get('/orders/{order_id}')
def order_detail(order_id: str, user_id: str = Depends(uid), actor_role: str = Depends(role), db: Session = Depends(get_db)):
    order=OrderRepository(db).get(order_id)
    if not order: raise HTTPException(status_code=404, detail='Order not found')
    if actor_role not in {'ADMIN','SUPPORT'} and order.user_id != user_id: raise HTTPException(status_code=403, detail='Not allowed')
    return ok('Order retrieved', out(order))
@router.patch('/orders/{order_id}/status')
def update_status(order_id: str, payload: StatusUpdate, user_id: str = Depends(uid), actor_role: str = Depends(role), db: Session = Depends(get_db)):
    if actor_role not in {'ADMIN','SUPPORT','SELLER'}: raise HTTPException(status_code=403, detail='Insufficient role')
    repo=OrderRepository(db); order=repo.get(order_id)
    if not order: raise HTTPException(status_code=404, detail='Order not found')
    return ok('Order status updated', out(repo.status(order, payload.status, user_id, payload.message)))
@router.post('/orders/{order_id}/cancel')
def cancel_order(order_id: str, user_id: str = Depends(uid), db: Session = Depends(get_db)):
    repo=OrderRepository(db); order=repo.get(order_id)
    if not order: raise HTTPException(status_code=404, detail='Order not found')
    if order.status not in {OrderStatus.PENDING, OrderStatus.CONFIRMED}: raise HTTPException(status_code=409, detail='Order cannot be cancelled at this stage')
    return ok('Order cancelled', out(repo.status(order, OrderStatus.CANCELLED, user_id, 'Customer cancelled order')))
@router.get('/admin/orders')
def admin_orders(status: OrderStatus | None = Query(default=None), actor_role: str = Depends(role), db: Session = Depends(get_db)):
    if actor_role not in {'ADMIN','SUPPORT'}: raise HTTPException(status_code=403, detail='Insufficient role')
    orders=OrderRepository(db).list(None)
    if status: orders=[o for o in orders if o.status == status]
    return ok('Admin orders retrieved', [out(o) for o in orders])
