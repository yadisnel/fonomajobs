from typing import List

from models.orders import OrderCreated, OrderToCreate


class OrdersController:
    # Singleton instance
    _self = None

    # Singleton instance
    def __new__(cls):
        if cls._self is None:
            cls._self = super().__new__(cls)
        return cls._self

    def __init__(self):
        # Initialize your database connection etc
        pass

    def get_orders(self):
        pass

    def get_order(self, order_id):
        pass

    def create_order(self, order: OrderToCreate):
        pass

    def update_order(self, order_id: int, order: OrderCreated):
        pass

    def delete_order(self, order_id: int):
        pass

    def process_orders(self, orders: List[OrderCreated], criterion: str):
        return sum(
            order.price * order.quantity
            for order in orders
            if order.status == criterion or criterion == "all"
        )
