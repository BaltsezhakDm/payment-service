from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.payment import PaymentType
from app.models.bank_payment import BankPaymentStatus


class CreatePaymentRequest(BaseModel):
    amount: Decimal
    type: PaymentType


class AmountRequest(BaseModel):
    amount: Decimal


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    amount: Decimal
    type: PaymentType
    status: str


class CreateAcquiringPaymentRequest(BaseModel):
    amount: Decimal


class BankPaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    payment_id: int
    bank_payment_id: str
    status: BankPaymentStatus
    paid_at: datetime | None