from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.api.products import router as products_router
from app.api.auth import router as auth_router
from app.core.security import get_current_user
from app.models.user import User
from app.api.cart import router as cart_router
from app.api.orders import router as orders_router
from app.api.payments import router as payments_router


app = FastAPI()
app.include_router(products_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(orders_router)
app.include_router(payments_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/db-health")
def db_health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}
  
@app.get("/auth/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "is_admin": current_user.is_admin}