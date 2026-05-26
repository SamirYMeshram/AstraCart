from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field
from app.models import ProductStatus

class CategoryCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    slug: str = Field(min_length=2, max_length=140)
    description: str | None = None
    icon: str | None = None

class CategoryOut(CategoryCreate):
    id: str
    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    title: str = Field(min_length=3, max_length=220)
    slug: str = Field(min_length=3, max_length=240)
    description: str = Field(min_length=10)
    price: float = Field(gt=0)
    discount_price: float | None = Field(default=None, gt=0)
    stock_quantity: int = Field(ge=0)
    category_id: str
    seller_id: str | None = None
    images: list[str] = []
    rating: float = Field(default=0, ge=0, le=5)
    status: ProductStatus = ProductStatus.ACTIVE
    sku: str

class ProductUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    discount_price: float | None = Field(default=None, gt=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    category_id: str | None = None
    images: list[str] | None = None
    rating: float | None = Field(default=None, ge=0, le=5)
    status: ProductStatus | None = None

class ProductOut(BaseModel):
    id: str
    title: str
    slug: str
    description: str
    price: float
    discount_price: float | None
    stock_quantity: int
    category_id: str
    seller_id: str
    images: list[str]
    rating: float
    status: ProductStatus
    sku: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class InventoryAdjustment(BaseModel):
    quantity: int = Field(gt=0)
    reason: str = 'order_created'
