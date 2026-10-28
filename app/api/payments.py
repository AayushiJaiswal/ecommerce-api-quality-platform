import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.order import Order, OrderStatus
from app.models.payment import Payment, PaymentStatus
from app.schemas.payment import PaymentCreate, PaymentOut

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.post("/", response_model=PaymentOut, status_code=201)
def create_payment(payload: PaymentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    existing = db.query(Payment).filter(Payment.idempotency_key == payload.idempotency_key).first()
    if existing:
        return existing

    order = db.query(Order).filter(Order.id == payload.order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != OrderStatus.pending_payment:
        raise HTTPException(status_code=409, detail=f"Order is already {order.status.value}, cannot pay again")

    from datetime import datetime, timezone
    if datetime.now(timezone.utc) > order.expires_at:
        order.status = OrderStatus.expired
        db.commit()
        raise HTTPException(status_code=409, detail="Order has expired, payment window closed")

    simulated_success = random.random() > 0.2

    payment = Payment(
        order_id=order.id,
        idempotency_key=payload.idempotency_key,
        status=PaymentStatus.success if simulated_success else PaymentStatus.declined,
    )
    db.add(payment)

    if simulated_success:
        order.status = OrderStatus.paid

    db.commit()
    db.refresh(payment)
    return payment


@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment or payment.order.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment