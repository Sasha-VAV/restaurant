from dataclasses import dataclass


@dataclass(frozen=True)
class Food:
    id: str
    name: str
    price: float


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    items: list[Food]


@dataclass(frozen=True)
class FinishedOrder:
    id: str
    tray_id: str
