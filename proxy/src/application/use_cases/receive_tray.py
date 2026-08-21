from src.application.ports import OrderBroadcaster
from src.domain import FinishedOrder


class ReceiveTray:
    def __init__(self, order_broadcaster: OrderBroadcaster):
        self._order_broadcaster = order_broadcaster

    async def receive_tray(self, finished_order: FinishedOrder):
        await self._order_broadcaster.broadcast_order(finished_order)
