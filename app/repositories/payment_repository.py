from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.payment import Payment, PaymentOperation


class SqlAlchemyPaymentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(self, payment_id: int) -> Payment | None:
        return self.session.get(Payment, payment_id)

    def save(self, payment: Payment) -> Payment:
        self.session.add(payment)
        self.session.flush()
        self.session.refresh(payment)
        return payment


class SqlAlchemyPaymentOperationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(self, operation: PaymentOperation) -> PaymentOperation:
        self.session.add(operation)
        self.session.flush()
        self.session.refresh(operation)
        return operation

    def list_by_payment_id(self, payment_id: int) -> list[PaymentOperation]:
        stmt = select(PaymentOperation).where(PaymentOperation.payment_id == payment_id)
        return list(self.session.scalars(stmt).all())