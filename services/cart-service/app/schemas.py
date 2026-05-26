from pydantic import BaseModel, Field
class CartItemCreate(BaseModel):
    product_id: str
    quantity: int = Field(gt=0, le=99)
class CartItemUpdate(BaseModel):
    quantity: int = Field(gt=0, le=99)
class CartItemOut(BaseModel):
    id: str; user_id: str; product_id: str; title: str; unit_price: float; quantity: int; stock_at_add: int; thumbnail: str | None = None
    line_total: float
class CartOut(BaseModel):
    items: list[CartItemOut]
    subtotal: float
    item_count: int
    stock_valid: bool
