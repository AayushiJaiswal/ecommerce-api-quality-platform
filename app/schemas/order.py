from datetime import datetime
from pydantic import BaseModel
from app.models.order import OrderStatus

class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_paise_at_purchase: int

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    status: OrderStatus
    created_at: datetime
    expires_at: datetime
    items: list[OrderItemOut]

    class Config:
        from_attributes = True