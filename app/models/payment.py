import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from app.core.database import Base

class PaymentStatus(str, enum.Enum):
    success = "success"
    declined = "declined"
    pending = "pending"
    failed = "failed"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    idempotency_key = Column(String, unique=True, nullable=False, index=True)
    status = Column(Enum(PaymentStatus), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))