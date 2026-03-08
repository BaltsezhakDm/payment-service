from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.models.payment import PaymentType


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
    deposited_amount: Decimal
    refunded_amount: Decimal