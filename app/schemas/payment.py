from pydantic import BaseModel
from app.models.payment import PaymentStatus

class PaymentCreate(BaseModel):
    order_id: int
    idempotency_key: str

class PaymentOut(BaseModel):
    id: int
    order_id: int
    status: PaymentStatus

    class Config:
        from_attributes = True