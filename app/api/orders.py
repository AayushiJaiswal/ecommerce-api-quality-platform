from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderOut

router = APIRouter(prefix="/orders", tags=["Orders"])

ORDER_EXPIRY_MINUTES = 15


@router.post("/", response_model=OrderOut, status_code=201)
def create_order(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    try:
        order = Order(
            user_id=current_user.id,
            status=OrderStatus.pending_payment,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=ORDER_EXPIRY_MINUTES),
        )
        db.add(order)
        db.flush()

        for cart_item in cart.items:
            product = (
                db.query(Product)
                .filter(Product.id == cart_item.product_id, Product.is_active == True)
                .with_for_update()
                .first()
            )
            if not product:
                raise HTTPException(status_code=404, detail=f"Product {cart_item.product_id} no longer available")
            if cart_item.quantity > product.stock:
                raise HTTPException(status_code=409, detail=f"Insufficient stock for {product.name}")

            product.stock -= cart_item.quantity

            db.add(OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=cart_item.quantity,
                price_paise_at_purchase=product.price_paise,
            ))

        for cart_item in list(cart.items):
            db.delete(cart_item)

        db.commit()
        db.refresh(order)
        return order

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Order creation failed")


@router.get("/", response_model=list[OrderOut])
def list_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
        .all()
    )


@router.get("/{order_id}", response_model=OrderOut)
def get_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order