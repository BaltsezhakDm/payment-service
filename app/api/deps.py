from collections.abc import Generator
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends

from app.db.session import SessionLocal
from app.repositories.order_repository import SqlAlchemyOrderRepository
from app.repositories.payment_repository import (
    SqlAlchemyPaymentRepository,
    SqlAlchemyPaymentOperationRepository,
)
from app.repositories.bank_payment_repository import (
    SqlAlchemyBankPaymentRepository,
)
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
    bank_payment_repo = SqlAlchemyBankPaymentRepository(db)

    return PaymentService(
        order_repo=order_repo,
        payment_repo=payment_repo,
        payment_operation_repo=payment_operation_repo,
        bank_payment_repo=bank_payment_repo,
    )