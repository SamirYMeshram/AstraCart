from __future__ import annotations
from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from app.models import Category, Product, ProductStatus
from app.schemas import CategoryCreate, ProductCreate, ProductUpdate

class CategoryRepository:
    def __init__(self, db: Session): self.db = db
    def list(self) -> list[Category]: return list(self.db.scalars(select(Category).order_by(Category.name)))
    def by_slug(self, slug: str) -> Category | None: return self.db.scalar(select(Category).where(Category.slug == slug))
    def create(self, payload: CategoryCreate) -> Category:
        category = Category(**payload.model_dump())
        self.db.add(category); self.db.commit(); self.db.refresh(category); return category

class ProductRepository:
    def __init__(self, db: Session): self.db = db
    def list(self, category_id: str | None = None, status: ProductStatus | None = ProductStatus.ACTIVE, low_stock: bool = False, limit: int = 100) -> list[Product]:
        stmt = select(Product).order_by(Product.created_at.desc()).limit(limit)
        if category_id: stmt = stmt.where(Product.category_id == category_id)
        if status: stmt = stmt.where(Product.status == status)
        if low_stock: stmt = stmt.where(Product.stock_quantity <= 5)
        return list(self.db.scalars(stmt))
    def get(self, product_id: str) -> Product | None: return self.db.get(Product, product_id)
    def by_slug(self, slug: str) -> Product | None: return self.db.scalar(select(Product).where(Product.slug == slug))
    def search(self, q: str, category_id: str | None = None, limit: int = 50) -> list[Product]:
        pattern = f'%{q.lower()}%'
        stmt = select(Product).where(or_(Product.title.ilike(pattern), Product.description.ilike(pattern), Product.sku.ilike(pattern))).limit(limit)
        if category_id: stmt = stmt.where(Product.category_id == category_id)
        return list(self.db.scalars(stmt))
    def create(self, payload: ProductCreate, seller_id: str) -> Product:
        data = payload.model_dump(); data['seller_id'] = seller_id
        product = Product(**data)
        self.db.add(product); self.db.commit(); self.db.refresh(product); return product
    def update(self, product: Product, payload: ProductUpdate) -> Product:
        for k,v in payload.model_dump(exclude_unset=True).items(): setattr(product, k, v)
        if product.stock_quantity <= 0: product.status = ProductStatus.OUT_OF_STOCK
        self.db.commit(); self.db.refresh(product); return product
    def delete(self, product: Product) -> None:
        product.status = ProductStatus.ARCHIVED
        self.db.commit()
    def decrement(self, product: Product, qty: int) -> Product:
        if product.stock_quantity < qty: raise ValueError('Insufficient stock')
        product.stock_quantity -= qty
        if product.stock_quantity == 0: product.status = ProductStatus.OUT_OF_STOCK
        self.db.commit(); self.db.refresh(product); return product
