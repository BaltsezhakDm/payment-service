from decimal import Decimal
from app.models.order import Order

def make_order(
    id: int = 1,
    amount: str = "1000.00",
    payment_status: str = "unpaid",
    payments=None,
) -> Order:
    return Order(
        id=id,
        amount=Decimal(amount),
        payment_status=payment_status,
        payments=payments or [],
    )