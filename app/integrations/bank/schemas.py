from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime

class BankPaymentStatus(BaseModel):
    bank_payment_id: str
    amount: Decimal
    status: str
    paid_at: datetime | None