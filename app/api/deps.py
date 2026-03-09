from collections.abc import Generator
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends

from app.core.config import settings
from app.db.session import SessionLocal
from app.repositories.order_repository import SqlAlchemyOrderRepository
from app.repositories.payment_repository import (
    SqlAlchemyPaymentRepository,
    SqlAlchemyPaymentOperationRepository,
)
from app.repositories.bank_payment_repository import (
    SqlAlchemyBankPaymentRepository,
)
from app.integrations.bank.client import BankApiClient
from app.services.bank_service import BankPaymentService
from app.services.payment_service import PaymentService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_payment_service(db: Annotated[Session, Depends(get_db)]) -> PaymentService:
    order_repo = SqlAlchemyOrderRepository(db)
    payment_repo = SqlAlchemyPaymentRepository(db)
    payment_operation_repo = SqlAlchemyPaymentOperationRepository(db)

    return PaymentService(
        order_repo=order_repo,
        payment_repo=payment_repo,
        payment_operation_repo=payment_operation_repo,
    )

def get_bank_payment_service(
    db: Annotated[Session, Depends(get_db)],
) -> BankPaymentService:
    order_repo = SqlAlchemyOrderRepository(db)
    payment_repo = SqlAlchemyPaymentRepository(db)
    payment_operation_repo = SqlAlchemyPaymentOperationRepository(db)
    bank_payment_repo = SqlAlchemyBankPaymentRepository(db)
    bank_api_client = BankApiClient(settings.BANK_URL)

    payment_service = PaymentService(
        order_repo=order_repo,
        payment_repo=payment_repo,
        payment_operation_repo=payment_operation_repo,
    )

    return BankPaymentService(
        payment_service=payment_service,
        payment_repo=payment_repo,
        bank_payment_repo=bank_payment_repo,
        bank_api_client=bank_api_client
    )