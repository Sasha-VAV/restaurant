import random

import asyncio

from src.application.ports.staff import Staff
from src.domain.entities.order import Order, FinishedOrder


class StaffMock(Staff):
    def __init__(self):
        self.counter = 0

    async def prepare_order(self, order: Order) -> FinishedOrder:
        delay = random.uniform(0.01, 1.0)
        await asyncio.sleep(delay)
        tray_id = str(self.counter)
        self.counter += 1

        return FinishedOrder(id=order.id, tray_id=tray_id)
