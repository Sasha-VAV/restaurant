from abc import ABC, abstractmethod
import typing as tp

from src.domain import FinishedOrder


class StreamShelf(ABC):
    @abstractmethod
    def stream(self) -> tp.AsyncIterator[FinishedOrder]:
        """Stream items from the shelf."""
        pass
