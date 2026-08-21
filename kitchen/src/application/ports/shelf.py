from abc import ABC, abstractmethod

from src.domain.entities.order import FinishedOrder


class Shelf(ABC):
    @abstractmethod
    async def add_order(self, order: FinishedOrder) -> None:
        pass
