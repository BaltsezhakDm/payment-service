from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class PaymentType(str, Enum):
    CASH = "cash"
    ACQUIRING = "acquiring"


@dataclass
class Payment:
    id: int | None
    order_id: int
    amount: Decimal
    type: PaymentType
    status: str = "pending"

    deposited_amount: Decimal = Decimal("0")
    refunded_amount: Decimal = Decimal("0")