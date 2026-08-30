import asyncio

from src.application.ports import OrderBroadcaster
from src.domain import FinishedOrder


_print_lock = asyncio.Lock()


class MockBroadcaster(OrderBroadcaster):
    async def broadcast_order(self, order: FinishedOrder):
        async with _print_lock:
            print(
                f"Broadcasting tray for order {order.id} with tray ID {order.tray_id}"
            )
