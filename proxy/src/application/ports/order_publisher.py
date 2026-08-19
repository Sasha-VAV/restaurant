from abc import ABC, abstractmethod
from src.domain import Order


class OrderPublisher(ABC):
    @abstractmethod
    async def publish(self, order: Order):
        pass
