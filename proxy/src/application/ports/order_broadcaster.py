from abc import ABC, abstractmethod


from src.domain import FinishedOrder


class OrderBroadcaster(ABC):
    @abstractmethod
    async def broadcast_order(self, order: FinishedOrder):
        pass
