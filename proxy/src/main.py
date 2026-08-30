import asyncio
from contextlib import AsyncExitStack
import signal
import uvicorn

from src.config import Settings
from src.api.app import create_app
from src.infrastructure.stream_shelf.kafka_consumer import KafkaTrayReceiver
from src.infrastructure.order_publisher.kafka_publisher import KafkaOrderPublisher
from src.infrastructure.order_broadcaster.mock_broadcaster import MockBroadcaster
from src.application.use_cases import ReceiveTray, CreateOrder
from src.grpc_server.server import GRPCServer


async def main():
    settings = Settings()

    order_broadcaster = MockBroadcaster()

    kafka_consumer = KafkaTrayReceiver(settings=settings.kafka)
    receive_tray_use_case = ReceiveTray(
        shelf_stream=kafka_consumer, order_broadcaster=order_broadcaster
    )

    publisher = KafkaOrderPublisher(settings=settings.kafka)
    create_order_use_case = CreateOrder(order_publisher=publisher)

    app = create_app(
        create_order_use_case
    )  # Should be reworked, but preserved that way to follow fastapi best practices
    app.state.order_publisher = publisher
    uvicorn_config = uvicorn.Config(
        app, host=settings.fastapi.host, port=settings.fastapi.port
    )
    uvicorn_server = uvicorn.Server(uvicorn_config)

    grpc_server = GRPCServer(
        create_order=create_order_use_case,
        receive_tray=receive_tray_use_case,
        port=settings.grpc.port,
    )

    stop_event = asyncio.Event()
    loop = asyncio.get_event_loop()

    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, stop_event.set)

    async with AsyncExitStack() as stack:
        await publisher.start()
        stack.push_async_callback(publisher.stop)

        await kafka_consumer.start()
        stack.push_async_callback(kafka_consumer.stop)

        await grpc_server.start()

        api_task = asyncio.create_task(uvicorn_server.serve())

        await stop_event.wait()

        uvicorn_server.should_exit = True
        await api_task


if __name__ == "__main__":
    asyncio.run(main())
