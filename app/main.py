from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import get_db
from app.api.products import router as products_router
from app.api.auth import router as auth_router
app = FastAPI()
app.include_router(products_router)
app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/db-health")
def db_health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}