from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.payment import PaymentType, PaymentStatus
from app.models.bank_payment import BankPaymentStatus


class CreatePaymentRequest(BaseModel):
    amount: Decimal = Field(
        gt=0,
        description="Сумма платежа. Должна быть строго больше нуля.",
        examples=["300.00"],
    )
    type: PaymentType = Field(description="Тип платежа: cash или acquiring")


class AmountRequest(BaseModel):
    amount: Decimal = Field(
        gt=0,
        description="Сумма операции (deposit/refund). Должна быть строго больше нуля.",
        examples=["150.00"],
    )



class PaymentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "order_id": 10,
                "amount": "500.00",
                "type": "cash",
                "status": "pending",
            }
        },
    )

    id: int
    order_id: int
    amount: Decimal
    type: PaymentType
    status: PaymentStatus


class CreateAcquiringPaymentRequest(BaseModel):
    amount: Decimal = Field(
        gt=0,
        description="Сумма эквайрингового платежа. Должна быть строго больше нуля.",
        examples=["300.00"],
    )


class BankPaymentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "payment_id": 15,
                "bank_payment_id": "bank-12345",
                "status": "paid",
                "paid_at": "2026-03-09T12:00:00",
            }
        },
    )

    id: int
    payment_id: int
    bank_payment_id: str
    status: BankPaymentStatus
    paid_at: datetime | None


class ErrorResponse(BaseModel):
    detail: str = Field(description="Текст ошибки")