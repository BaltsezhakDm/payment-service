from fastapi import APIRouter, Depends, Path, status

from app.api.deps import get_payment_service, get_bank_payment_service
from app.schemas.payment import (
    AmountRequest, 
    CreatePaymentRequest, 
    PaymentResponse,
    CreateAcquiringPaymentRequest,
    BankPaymentResponse,
    ErrorResponse,
)
from app.services.payment_service import PaymentService
from app.services.bank_service import BankPaymentService

router = APIRouter(tags=["payments"])

COMMON_PAYMENT_ERRORS = {
    400: {
        "model": ErrorResponse,
        "description": "Ошибка валидации",
    },
    404: {"model": ErrorResponse, "description": "Заказ или платеж не найден"},
    409: {"model": ErrorResponse, "description": "Переплата по заказу"},
    422: {"model": ErrorResponse, "description": "Ошибка валидации входного payload"},
}

@router.post(
    "/orders/{order_id}/payments",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать платеж по заказу",
    description="Создает платеж для существующего заказа.",
    responses=COMMON_PAYMENT_ERRORS,
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
    "/orders/{order_id}/acquiring-payments",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать эквайринговый платеж",
    description="Создает локальный платеж и инициирует платеж в API банка.",
    responses={
        **COMMON_PAYMENT_ERRORS,
        502: {"model": ErrorResponse, "description": "Ошибка внешнего API банка"},
    },
)
def create_acquiring_payment(
    order_id: int = Path(description="ID заказа", examples=[1]),
    payload: CreateAcquiringPaymentRequest = ...,
    service: BankPaymentService = Depends(get_bank_payment_service),
) -> PaymentResponse:
    payment = service.create_acquiring_payment(
        order_id=order_id,
        amount=payload.amount,
    )
    return PaymentResponse.model_validate(payment)


@router.post(
    "/payments/{payment_id}/deposit",
    response_model=PaymentResponse,
    summary="Зачислить средства по платежу",
    description="Выполняет операцию внесения и пересчитывает статус заказа/платежа.",
    responses=COMMON_PAYMENT_ERRORS,
)
def deposit_payment(
    payment_id: int = Path(description="ID платежа", examples=[1]),
    payload: AmountRequest = ...,
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
    summary="Вернуть средства по платежу",
    description="Выполняет операцию возврата и пересчитывает статус заказа/платежа.",
    responses=COMMON_PAYMENT_ERRORS,
)
def refund_payment(
    payment_id: int = Path(description="ID платежа", examples=[1]),
    payload: AmountRequest = ...,
    service: PaymentService = Depends(get_payment_service),
) -> PaymentResponse:
    payment = service.refund_payment(
        payment_id=payment_id,
        amount=payload.amount,
    )
    return PaymentResponse.model_validate(payment)

@router.post(
    "/payments/{payment_id}/acquiring-sync",
    response_model=BankPaymentResponse,
    summary="Синхронизировать эквайринговый платеж",
    description="Запрашивает текущее состояние платежа в банке и согласовывает локальное состояние.",
    responses={
        404: {"model": ErrorResponse, "description": "Платеж/банковский платеж не найден"},
        502: {"model": ErrorResponse, "description": "Ошибка внешнего API банка"},
    },
)
def sync_acquiring_payment(
    payment_id: int = Path(description="ID платежа", examples=[1]),
    service: BankPaymentService = Depends(get_bank_payment_service),
) -> BankPaymentResponse:
    bank_payment = service.sync_payment(payment_id)
    return BankPaymentResponse.model_validate(bank_payment)