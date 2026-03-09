from decimal import Decimal

import requests

from app.integrations.bank.schemas import AcquiringCheckResult
from app.services.exceptions import (
    BankPaymentError,
    BankPaymentNotFoundError,
)


class BankApiClient:
    def __init__(self, base_url: str, timeout: int = 5) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def acquiring_start(self, order_number: str, amount: Decimal) -> str:
        try:
            response = requests.post(
                f"{self.base_url}/acquiring_start",
                json={
                    "order_number": order_number,
                    "amount": str(amount),
                },
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            raise BankPaymentError("Ошибка при обращении к банку")
        except ValueError:
            raise BankPaymentError("Банк вернул невалидный JSON")

        bank_payment_id = data.get("bank_payment_id")
        if not bank_payment_id:
            raise BankPaymentError("Банк не вернул bank_payment_id")

        return bank_payment_id

    def acquiring_check(self, bank_payment_id: str) -> AcquiringCheckResult:
        try:
            response = requests.get(
                f"{self.base_url}/acquiring_check",
                params={"bank_payment_id": bank_payment_id},
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            raise BankPaymentError("Ошибка при обращении к банку")
        except ValueError:
            raise BankPaymentError("Банк вернул невалидный JSON")

        error = data.get("error")
        if error:
            if str(error).strip().lower() == "платеж не найден":
                raise BankPaymentNotFoundError()
            raise BankPaymentError(str(error))

        try:
            return AcquiringCheckResult.model_validate(data)
        except Exception:
            raise BankPaymentError("Банк вернул невалидную структуру ответа")