from fastapi import FastAPI, HTTPException

from app.api.routes.payments import router as payments_router
from app.services.exceptions import (
    InvalidDepositAmountError,
    InvalidRefundAmountError,
    OrderNotFoundError,
    OverpaymentError,
    PaymentNotFoundError,
)

app = FastAPI(title="Payment Service")


@app.exception_handler(OrderNotFoundError)
async def order_not_found_handler(request, exc):
    raise HTTPException(status_code=404, detail="Order not found")


@app.exception_handler(PaymentNotFoundError)
async def payment_not_found_handler(request, exc):
    raise HTTPException(status_code=404, detail="Payment not found")


@app.exception_handler(OverpaymentError)
async def overpayment_handler(request, exc):
    raise HTTPException(
        status_code=409,
        detail="Total payments cannot exceed order amount",
    )


@app.exception_handler(InvalidDepositAmountError)
async def invalid_deposit_handler(request, exc):
    raise HTTPException(
        status_code=400,
        detail="Deposit amount exceeds payment amount",
    )


@app.exception_handler(InvalidRefundAmountError)
async def invalid_refund_handler(request, exc):
    raise HTTPException(
        status_code=400,
        detail="Refund amount exceeds deposited amount",
    )


app.include_router(payments_router)