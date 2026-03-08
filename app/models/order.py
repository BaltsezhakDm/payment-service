from dataclasses import dataclass, field
from decimal import Decimal
from typing import List

from app.models.payment import Payment


@dataclass
class Order:
    id: int
    amount: Decimal
    payment_status: str
    payments: List[Payment] = field(default_factory=list)