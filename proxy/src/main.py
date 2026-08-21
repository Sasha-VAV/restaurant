import asyncio
from contextlib import AsyncExitStack
import signal
import uvicorn

from src.config import Settings
from src.api.app import create_app
from src.infrastructure.order_consumer.kafka_consumer import KafkaTrayReceiver
from src.infrastructure.order_broadcaster.mock_broadcaster import MockBroadcaster
from src.application.use_cases.receive_tray import ReceiveTray


async def main():
    settings = Settings()

    order_broadcaster = MockBroadcaster()
    receive_tray_use_case = ReceiveTray(order_broadcaster)
    kafka_consumer = KafkaTrayReceiver(
        settings=settings.kafka, receive_tray_use_case=receive_tray_use_case
    )

    app = create_app(settings)
    uvicorn_config = uvicorn.Config(app, host=settings.app.host, port=settings.app.port)
    uvicorn_server = uvicorn.Server(uvicorn_config)

    stop_event = asyncio.Event()
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)

    async with AsyncExitStack() as stack:
        await kafka_consumer.start()
        stack.push_async_callback(kafka_consumer.stop)

        api_task = asyncio.create_task(uvicorn_server.serve())

        await stop_event.wait()

        uvicorn_server.should_exit = True
        await api_task


if __name__ == "__main__":
    asyncio.run(main())
