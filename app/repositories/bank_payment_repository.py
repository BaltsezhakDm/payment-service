from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.bank_payment import BankPayment


class SqlAlchemyBankPaymentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, bank_payment_id: int) -> BankPayment | None:
        return self.session.get(BankPayment, bank_payment_id)

    def get_by_payment_id(self, payment_id: int) -> BankPayment | None:
        stmt = select(BankPayment).where(BankPayment.payment_id == payment_id)
        return self.session.scalar(stmt)

    def get_by_bank_payment_id(self, external_bank_payment_id: str) -> BankPayment | None:
        stmt = select(BankPayment).where(
            BankPayment.bank_payment_id == external_bank_payment_id
        )
        return self.session.scalar(stmt)

    def save(self, bank_payment: BankPayment) -> BankPayment:
        self.session.add(bank_payment)
        self.session.flush()
        self.session.refresh(bank_payment)
        return bank_payment