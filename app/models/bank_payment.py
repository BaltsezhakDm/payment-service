from datetime import datetime
from enum import Enum
from decimal import Decimal

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BankPaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class BankPayment(Base):
    __tablename__ = "bank_payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    payment_id: Mapped[int] = mapped_column(ForeignKey("payments.id"), nullable=False)
    bank_payment_id: Mapped[str] = mapped_column(nullable=False, unique=True)

    status: Mapped[BankPaymentStatus] = mapped_column(
        SqlEnum(BankPaymentStatus),
        default=BankPaymentStatus.PENDING,
        nullable=False,
    )
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    payment: Mapped["Payment"] = relationship(back_populates="bank_payments")