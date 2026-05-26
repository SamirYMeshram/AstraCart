from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.responses import ok
from app.repositories import CartRepository
from app.schemas import CartItemCreate, CartItemUpdate
from app.services import CartService, item_to_dict
router=APIRouter()
def user_id(x_user_id: str | None = Header(default=None)) -> str: return x_user_id or 'demo-customer'
@router.get('/cart')
def get_cart(uid: str = Depends(user_id), db: Session = Depends(get_db)): return ok('Cart retrieved', CartService(CartRepository(db)).view(uid))
@router.post('/cart/items', status_code=201)
async def add_item(payload: CartItemCreate, uid: str = Depends(user_id), db: Session = Depends(get_db)): return ok('Item added to cart', await CartService(CartRepository(db)).add(uid, payload.product_id, payload.quantity))
@router.patch('/cart/items/{item_id}')
def update_item(item_id: str, payload: CartItemUpdate, uid: str = Depends(user_id), db: Session = Depends(get_db)):
    repo=CartRepository(db); item=repo.get(item_id, uid)
    if not item: raise HTTPException(status_code=404, detail='Cart item not found')
    if payload.quantity > item.stock_at_add: raise HTTPException(status_code=409, detail='Requested quantity exceeds known stock')
    return ok('Cart item updated', item_to_dict(repo.update_qty(item, payload.quantity)))
@router.delete('/cart/items/{item_id}')
def delete_item(item_id: str, uid: str = Depends(user_id), db: Session = Depends(get_db)):
    repo=CartRepository(db); item=repo.get(item_id, uid)
    if not item: raise HTTPException(status_code=404, detail='Cart item not found')
    repo.delete(item); return ok('Cart item removed', {'id': item_id})
@router.delete('/cart/clear')
def clear_cart(uid: str = Depends(user_id), db: Session = Depends(get_db)):
    CartRepository(db).clear(uid); return ok('Cart cleared', {'user_id': uid})
@router.get('/internal/cart/{target_user_id}')
def internal_cart(target_user_id: str, db: Session = Depends(get_db)): return ok('Internal cart retrieved', CartService(CartRepository(db)).view(target_user_id))
