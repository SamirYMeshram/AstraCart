from __future__ import annotations
from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.responses import ok
from app.models import ProductStatus
from app.repositories import CategoryRepository, ProductRepository
from app.schemas import CategoryCreate, CategoryOut, InventoryAdjustment, ProductCreate, ProductOut, ProductUpdate

router = APIRouter()

def _actor(x_user_id: str | None = Header(default=None), x_user_role: str | None = Header(default=None)) -> tuple[str, str]:
    return x_user_id or 'seed-seller', x_user_role or 'ADMIN'

def _product_out(product):
    return ProductOut.model_validate(product).model_dump(mode='json')

@router.get('/categories')
def categories(db: Session = Depends(get_db)):
    return ok('Categories retrieved', [CategoryOut.model_validate(c).model_dump(mode='json') for c in CategoryRepository(db).list()])

@router.post('/categories', status_code=201)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db), actor = Depends(_actor)):
    if actor[1] not in {'ADMIN','SELLER'}: raise HTTPException(status_code=403, detail='Insufficient role')
    repo = CategoryRepository(db)
    existing = repo.by_slug(payload.slug)
    return ok('Category ready', CategoryOut.model_validate(existing or repo.create(payload)).model_dump(mode='json'))

@router.get('/products')
def products(category_id: str | None = None, status_filter: ProductStatus | None = Query(default=ProductStatus.ACTIVE, alias='status'), low_stock: bool = False, db: Session = Depends(get_db)):
    return ok('Products retrieved', [_product_out(p) for p in ProductRepository(db).list(category_id, status_filter, low_stock)])

@router.get('/products/search')
def search_products(q: str = Query(min_length=1), category_id: str | None = None, db: Session = Depends(get_db)):
    return ok('Product search complete', [_product_out(p) for p in ProductRepository(db).search(q, category_id)])

@router.get('/products/{product_id}')
def product_detail(product_id: str, db: Session = Depends(get_db)):
    product = ProductRepository(db).get(product_id)
    if not product: raise HTTPException(status_code=404, detail='Product not found')
    return ok('Product retrieved', _product_out(product))

@router.post('/products', status_code=201)
def create_product(payload: ProductCreate, db: Session = Depends(get_db), actor = Depends(_actor)):
    if actor[1] not in {'ADMIN','SELLER'}: raise HTTPException(status_code=403, detail='Only admins and sellers can create products')
    seller_id = payload.seller_id or actor[0]
    return ok('Product created', _product_out(ProductRepository(db).create(payload, seller_id)))

@router.patch('/products/{product_id}')
def update_product(product_id: str, payload: ProductUpdate, db: Session = Depends(get_db), actor = Depends(_actor)):
    repo = ProductRepository(db); product = repo.get(product_id)
    if not product: raise HTTPException(status_code=404, detail='Product not found')
    if actor[1] not in {'ADMIN','SELLER'} or (actor[1] == 'SELLER' and product.seller_id != actor[0]): raise HTTPException(status_code=403, detail='Not allowed to edit this product')
    return ok('Product updated', _product_out(repo.update(product, payload)))

@router.delete('/products/{product_id}')
def delete_product(product_id: str, db: Session = Depends(get_db), actor = Depends(_actor)):
    repo = ProductRepository(db); product = repo.get(product_id)
    if not product: raise HTTPException(status_code=404, detail='Product not found')
    if actor[1] not in {'ADMIN','SELLER'}: raise HTTPException(status_code=403, detail='Insufficient role')
    repo.delete(product)
    return ok('Product archived', {'id': product_id})

@router.post('/internal/products/{product_id}/decrement-stock')
def decrement_stock(product_id: str, payload: InventoryAdjustment, db: Session = Depends(get_db)):
    repo = ProductRepository(db); product = repo.get(product_id)
    if not product: raise HTTPException(status_code=404, detail='Product not found')
    try:
        updated = repo.decrement(product, payload.quantity)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return ok('Inventory decremented', _product_out(updated))

@router.get('/inventory/low-stock')
def low_stock(db: Session = Depends(get_db)):
    return ok('Low stock products retrieved', [_product_out(p) for p in ProductRepository(db).list(status=None, low_stock=True)])
