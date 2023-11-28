from controllers.orders import OrdersController
from models.orders import OrderCreated


def test_orders_controller_is_singleton():
    controller1 = OrdersController()
    controller2 = OrdersController()
    assert controller1 is controller2


def test_orders_controller_process_orders():
    controller = OrdersController()
    orders_list = [
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
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
    ]
    orders = [
        OrderCreated(
            id=order["id"],
            item=order["item"],
            quantity=order["quantity"],
            price=order["price"],
            status=order["status"],
        )
        for order in orders_list
    ]
    assert controller.process_orders(orders, "completed") == 1299.69
    assert controller.process_orders(orders, "all") == 2399.55
