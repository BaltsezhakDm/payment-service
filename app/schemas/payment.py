from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.payment import PaymentType, PaymentStatus
from app.models.bank_payment import BankPaymentStatus


class CreatePaymentRequest(BaseModel):
    amount: Decimal = Field(gt=0)
    type: PaymentType


class AmountRequest(BaseModel):
    amount: Decimal = Field(gt=0)


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_id: int
    amount: Decimal
    type: PaymentType
    status: PaymentStatus


class CreateAcquiringPaymentRequest(BaseModel):
    amount: Decimal = Field(gt=0)


class BankPaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    payment_id: int
    bank_payment_id: str
    status: BankPaymentStatus
    paid_at: datetime | None