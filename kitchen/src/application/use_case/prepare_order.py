from src.application.ports.staff import Staff
from src.application.ports.shelf import Shelf
from src.domain.entities.order import Order


class PrepareOrder:
    def __init__(self, staff: Staff, shelf: Shelf):
        self._staff = staff
        self._shelf = shelf

    async def prepare_order(self, order: Order):
        finished_order = await self._staff.prepare_order(order)
        await self._shelf.add_order(finished_order)
