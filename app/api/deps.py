from app.repositories.interfaces import OrderRepository, PaymentRepository
from app.services.payment_service import PaymentService

order_repo = OrderRepository()
payment_repo = PaymentRepository()


def get_payment_service() -> PaymentService:
    return PaymentService(order_repo=order_repo, payment_repo=payment_repo)