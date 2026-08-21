import asyncio
import signal
from contextlib import AsyncExitStack

from src.config import Settings
from src.infrastructure.order_consumer.kafka_consumer import KafkaOrderConsumer
from src.infrastructure.shelf.kafka_producer import ShelfKafkaProducer
from src.infrastructure.staff.staff_mock import StaffMock
from src.application.use_case.prepare_order import PrepareOrder


async def main():
    settings = Settings()

    staff = StaffMock()
    shelf = ShelfKafkaProducer(settings=settings.kafka)

    prepare_order = PrepareOrder(staff=staff, shelf=shelf)

    consumer = KafkaOrderConsumer(
        kafka_settings=settings.kafka, prepare_order=prepare_order
    )

    stop_event = asyncio.Event()
    loop = asyncio.get_event_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)

    async with AsyncExitStack() as stack:
        await shelf.start()
        stack.push_async_callback(shelf.stop)

        await consumer.start()
        stack.push_async_callback(consumer.stop)

        await stop_event.wait()


if __name__ == "__main__":
    asyncio.run(main())
