from fastapi import APIRouter, Depends, status

from app.api.deps import get_payment_service
from app.schemas.payment import AmountRequest, CreatePaymentRequest, PaymentResponse
from app.services.payment_service import PaymentService

router = APIRouter(tags=["payments"])


@router.post(
    "/orders/{order_id}/payments",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_payment(
    order_id: int,
    payload: CreatePaymentRequest,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    payment = service.create_payment(
        order_id=order_id,
        amount=payload.amount,
        payment_type=payload.type,
    )
    return PaymentResponse.model_validate(payment)


@router.post(
    "/payments/{payment_id}/deposit",
    response_model=PaymentResponse,
)
def deposit_payment(
    payment_id: int,
    payload: AmountRequest,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    payment = service.deposit_payment(
        payment_id=payment_id,
        amount=payload.amount,
    )
    return PaymentResponse.model_validate(payment)


@router.post(
    "/payments/{payment_id}/refund",
    response_model=PaymentResponse,
)
def refund_payment(
    payment_id: int,
    payload: AmountRequest,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    payment = service.refund_payment(
        payment_id=payment_id,
        amount=payload.amount,
    )
    return PaymentResponse.model_validate(payment)
