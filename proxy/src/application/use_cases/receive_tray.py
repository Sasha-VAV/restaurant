import typing as tp

from src.application.ports import StreamShelf, OrderBroadcaster
from src.domain import FinishedOrder


class ReceiveTray:
    def __init__(self, shelf_stream: StreamShelf, order_broadcaster: OrderBroadcaster):
        self._shelf_stream = shelf_stream
        self._order_broadcaster = order_broadcaster

    async def subscribe(self) -> tp.AsyncIterator[FinishedOrder]:
        async for finished_order in self._shelf_stream.stream():
            await self._receive_tray(finished_order)
            yield finished_order

    async def _receive_tray(self, finished_order: FinishedOrder):
        await self._order_broadcaster.broadcast_order(finished_order)
