from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.product import Product
from app.models.cart import Cart, CartItem
from app.schemas.cart import CartItemCreate, CartOut

router = APIRouter(prefix="/cart", tags=["Cart"])


def get_or_create_cart(user: User, db: Session) -> Cart:
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("/", response_model=CartOut)
def view_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = get_or_create_cart(current_user, db)
    return cart


@router.post("/items", response_model=CartOut, status_code=201)
def add_item(payload: CartItemCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if payload.quantity <= 0:
        raise HTTPException(status_code=422, detail="quantity must be positive")

    product = db.query(Product).filter(Product.id == payload.product_id, Product.is_active == True).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if payload.quantity > product.stock:
        raise HTTPException(status_code=409, detail="Requested quantity exceeds available stock")

    cart = get_or_create_cart(current_user, db)

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id, CartItem.product_id == payload.product_id
    ).first()

    if existing_item:
        new_quantity = existing_item.quantity + payload.quantity
        if new_quantity > product.stock:
            raise HTTPException(status_code=409, detail="Requested quantity exceeds available stock")
        existing_item.quantity = new_quantity
    else:
        existing_item = CartItem(cart_id=cart.id, product_id=payload.product_id, quantity=payload.quantity)
        db.add(existing_item)

    db.commit()
    db.refresh(cart)
    return cart


@router.delete("/items/{item_id}", response_model=CartOut)
def remove_item(item_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    cart = get_or_create_cart(current_user, db)
    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(item)
    db.commit()
    db.refresh(cart)
    return cart