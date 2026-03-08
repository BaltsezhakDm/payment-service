import pytest
from fastapi.testclient import TestClient
from decimal import Decimal

from app.services.payment_service import PaymentService
from app.repositories.memory import (
    InMemoryOrderRepository, 
    InMemoryPaymentRepository,
    )
from app.models.order import Order
from app.api.deps import get_payment_service
from app.main import app


@pytest.fixture
def repos():
    order_repo = InMemoryOrderRepository()
    payment_repo = InMemoryPaymentRepository()
    return order_repo, payment_repo

@pytest.fixture
def payment_service(repos):
    order_repo, payment_repo = repos

    return PaymentService(order_repo, payment_repo)

@pytest.fixture 
def client(repos):     
    order_repo, payment_repo = repos      
    service = PaymentService(order_repo, payment_repo)      

    app.dependency_overrides[get_payment_service] = lambda: service  

    client = TestClient(app) 

    yield client    

    app.dependency_overrides.clear()

@pytest.fixture
def order_1000(repos):
    order_repo, _ = repos

    order = Order(
        id=1,
        amount=Decimal("1000.00"),
        payment_status="unpaid",
        payments=[],
    )

    order_repo.save(order)

    return order