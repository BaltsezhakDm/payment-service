from decimal import Decimal

from app.models.order import Order, OrderPaymentStatus
from app.models.payment import Payment, PaymentType
from app.services.exceptions import (
    OverpaymentError,
    InvalidDepositAmountError,
    InvalidRefundAmountError,
    OrderNotFoundError,
    PaymentNotFoundError,
)
from app.repositories.order_repository import SqlAlchemyOrderRepository
from app.repositories.payment_repository import SqlAlchemyPaymentRepository


class PaymentService:
    def __init__(
        self,
        order_repo: SqlAlchemyOrderRepository,
        payment_repo: SqlAlchemyPaymentRepository,
    ) -> None:
        self.order_repo = order_repo
        self.payment_repo = payment_repo

    def create_payment(
        self,
        order_id: int,
        amount: Decimal,
        payment_type: PaymentType,
    ) -> Payment:
        order = self.order_repo.get_by_id(order_id)
        if order is None:
            raise OrderNotFoundError()

        current_total = sum(payment.amount for payment in order.payments)
        if current_total + amount > order.amount:
            raise OverpaymentError()

        payment = Payment(
            order_id=order.id,
            amount=amount,
            type=payment_type,
        )

        payment = self.payment_repo.save(payment)
        order.payments.append(payment)
        return payment

    def deposit_payment(self, payment_id: int, amount: Decimal) -> Payment:
        payment = self.payment_repo.get_by_id(payment_id)
        if payment is None:
            raise PaymentNotFoundError()

        order = self.order_repo.get_by_id(payment.order_id)
        if order is None:
            raise OrderNotFoundError()

        if payment.deposited_amount + amount > payment.amount:
            raise InvalidDepositAmountError()

        total_paid = self._total_paid(order)
        if total_paid + amount > order.amount:
            raise OverpaymentError()

        payment.deposited_amount += amount
        payment = self.payment_repo.save(payment)

        self._update_order_status(order)
        self.order_repo.save(order)

        return payment

    def refund_payment(self, payment_id: int, amount: Decimal) -> Payment:
        payment = self.payment_repo.get_by_id(payment_id)
        if payment is None:
            raise PaymentNotFoundError()

        order = self.order_repo.get_by_id(payment.order_id)
        if order is None:
            raise OrderNotFoundError()

        if payment.refunded_amount + amount > payment.deposited_amount:
            raise InvalidRefundAmountError()

        payment.refunded_amount += amount
        payment = self.payment_repo.save(payment)

        self._update_order_status(order)
        self.order_repo.save(order)

        return payment

    def _total_paid(self, order: Order) -> Decimal:
        return sum(
            payment.deposited_amount - payment.refunded_amount
            for payment in order.payments
        )

    def _update_order_status(self, order: Order) -> None:
        total_paid = self._total_paid(order)

        if total_paid == Decimal("0.00"):
            order.payment_status = OrderPaymentStatus.UNPAID
        elif total_paid < order.amount:
            order.payment_status = OrderPaymentStatus.PARTIALLY_PAID
        else:
            order.payment_status = OrderPaymentStatus.PAID