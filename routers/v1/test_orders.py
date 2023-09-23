from fastapi.testclient import TestClient
from starlette.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_412_PRECONDITION_FAILED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from main import app

client = TestClient(app)


def test_process_orders_list_empty():
    response = client.post(
        "/v1/solution",
        json={
            "orders": [],
            "criterion": "pending",
        },
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_process_orders_list_criterion_not_present():
    response = client.post(
        "/v1/solution",
        json={
            "orders": [
                {
                    "id": 1,
                    "item": "Laptop",
                    "quantity": 2,
                    "price": 1.5,
                    "status": "completed",
                }
            ],
            "criterion": "pending",
        },
    )
    assert response.status_code == HTTP_412_PRECONDITION_FAILED


def test_orders_inputs():
    test_cases = [
        (
            "bad item type",
            {
                "id": 1,
                "item": "something",
                "quantity": 1,
                "price": 2.5,
                "status": "pending",
            },
            HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            "quantity == 0",
            {
                "id": 1,
                "item": "Laptop",
                "quantity": 0,
                "price": 1.5,
                "status": "pending",
            },
            HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            "quantity < 0",
            {
                "id": 1,
                "item": "Laptop",
                "quantity": -1,
                "price": 1.5,
                "status": "pending",
            },
            HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            "price == 0",
            {
                "id": 1,
                "item": "Laptop",
                "quantity": -1,
                "price": 0.0,
                "status": "pending",
            },
            HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            "price < 0",
            {
                "id": 1,
                "item": "Laptop",
                "quantity": 1,
                "price": -1,
                "status": "pending",
            },
            HTTP_422_UNPROCESSABLE_ENTITY,
        ),
        (
            "bad status type",
            {
                "id": 1,
                "item": "Laptop",
                "quantity": 1,
                "price": 2.5,
                "status": "something",
            },
            HTTP_422_UNPROCESSABLE_ENTITY,
        ),
    ]
    for test_case in test_cases:
        name, order, status_code = test_case
        response = client.post(
            "/v1/solution",
            json={
                "orders": [order],
                "criterion": "pending",
            },
        )
        assert response.status_code == status_code


def test_complete_flow():
    response = client.post(
        "/v1/solution",
        json={
            "orders": [
                {
                    "id": 1,
                    "item": "Laptop",
                    "quantity": 1,
                    "price": 999.99,
                    "status": "completed",
                },
                {
                    "id": 2,
                    "item": "Smartphone",
                    "quantity": 2,
                    "price": 499.95,
                    "status": "pending",
                },
                {
                    "id": 3,
                    "item": "Headphones",
                    "quantity": 3,
                    "price": 99.90,
                    "status": "completed",
                },
                {
                    "id": 4,
                    "item": "Mouse",
                    "quantity": 4,
                    "price": 24.99,
                    "status": "canceled",
                },
            ],
            "criterion": "completed",
        },
    )
    assert response.status_code == HTTP_200_OK
    assert response.json() == {"total": 1299.69}
