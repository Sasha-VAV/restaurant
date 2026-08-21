from abc import ABC, abstractmethod

from src.domain.entities.order import Order, FinishedOrder


class Staff(ABC):
    @abstractmethod
    async def prepare_order(self, order: Order) -> FinishedOrder:
        pass
