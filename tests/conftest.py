import pytest
from app.services.payment_service import PaymentService
from tests.factories.order import make_order


@pytest.fixture
def payment_service():
    return PaymentService()


@pytest.fixture
def order_1000():
    return make_order(amount="1000.00")