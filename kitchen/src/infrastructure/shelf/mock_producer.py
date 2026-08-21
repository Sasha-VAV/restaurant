import asyncio

from src.application.ports.shelf import Shelf
from src.domain.entities.order import FinishedOrder

_print_lock = asyncio.Lock()


class MockShelf(Shelf):
    async def add_order(self, order: FinishedOrder):
        async with _print_lock:
            print(f"Order {order.id} added to shelf with tray_id {order.tray_id}")
