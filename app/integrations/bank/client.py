from decimal import Decimal

from app.integrations.bank.schemas import BankPaymentStatus


class BankApiClient:

    def acquiring_start(self, order_number: str, amount: Decimal) -> str:
        ...

    def acquiring_check(self, bank_payment_id: str) -> BankPaymentStatus:
        ...