from enum import Enum
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class BankPaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"


class AcquiringCheckResult(BaseModel):
    bank_payment_id: str
    amount: Decimal
    status: BankPaymentStatus
    paid_at: datetime | None = None