from decimal import Decimal
from unittest.mock import Mock


def test_create_acquiring_payment_endpoint(client, bank_api_client_mock, order_1000):
    bank_api_client_mock.acquiring_start.return_value = "bank-123"

    response = client.post(
        f"/orders/{order_1000.id}/acquiring-payments",
        json={"amount": "300.00"},
    )

    assert response.status_code == 201
    data = response.json()

    assert data["order_id"] == order_1000.id
    assert data["amount"] == "300.00"
    assert data["type"] == "acquiring"

    bank_api_client_mock.acquiring_start.assert_called_once_with(
        order_number=str(order_1000.id),
        amount=Decimal("300.00"),
    )


def test_sync_acquiring_payment_endpoint_marks_paid(
    client,
    bank_api_client_mock,
    order_1000,
):
    bank_api_client_mock.acquiring_start.return_value = "bank-123"

    create_response = client.post(
        f"/orders/{order_1000.id}/acquiring-payments",
        json={"amount": "300.00"},
    )
    assert create_response.status_code == 201
    payment_id = create_response.json()["id"]

    bank_api_client_mock.acquiring_check.return_value = Mock(
        bank_payment_id="bank-123",
        amount=Decimal("300.00"),
        status="paid",
        paid_at=None,
    )

    sync_response = client.post(f"/payments/{payment_id}/acquiring-sync")

    assert sync_response.status_code == 200
    data = sync_response.json()

    assert data["payment_id"] == payment_id
    assert data["bank_payment_id"] == "bank-123"
    assert data["status"] == "paid"


def test_sync_acquiring_payment_returns_404_for_unknown_payment(client):
    response = client.post("/payments/999999/acquiring-sync")

    assert response.status_code == 404
