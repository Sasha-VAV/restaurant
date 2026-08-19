from uuid import uuid4

from src.domain import Order, Food
from src.application.ports.order_publisher import OrderPublisher


class CreateOrder:
    def __init__(self, order_publisher: OrderPublisher):
        self.order_publisher = order_publisher

    async def create_order(self, customer_id: str, food_items: list[Food]) -> Order:
        order = Order(id=str(uuid4()), customer_id=customer_id, items=food_items)
        await self.order_publisher.publish(order)
        return order
