import asyncio
from aiokafka import AIOKafkaConsumer

from src.domain.entities.order import Order
from src.config import KafkaSettings
from src.application.use_case.prepare_order import PrepareOrder
from src.infrastructure.lifecycle import Startable
from src.infrastructure.messaging.create_order_utils import (
    verify_headers,
    extract_order_from_message,
)


EXPECTED_HEADERS = {
    "event_type": "order.created",
    "schema_version": "1",
}


class KafkaOrderConsumer(Startable):
    def __init__(self, kafka_settings: KafkaSettings, prepare_order: PrepareOrder):
        self._kafka_settings = kafka_settings
        self._prepare_order = prepare_order
        self._kafka_consumer: AIOKafkaConsumer | None = None
        self._task: asyncio.Task | None = None

    async def start(self):
        self._kafka_consumer = AIOKafkaConsumer(
            self._kafka_settings.topic,
            bootstrap_servers=self._kafka_settings.bootstrap_servers,
            group_id=self._kafka_settings.group_id,
            key_deserializer=lambda m: m,
            value_deserializer=lambda m: m,
            enable_auto_commit=False,
            auto_offset_reset="earliest",
        )
        await self._kafka_consumer.start()
        self._task = asyncio.create_task(self._consume_orders())

    async def stop(self):
        if self._kafka_consumer:
            await self._kafka_consumer.stop()
        if self._task:
            self._task.cancel()

    async def _consume_orders(self):
        print("Kafka consumer started, waiting for messages...")
        if self._kafka_consumer is None:
            raise RuntimeError("Kafka consumer is not initialized")

        async for msg in self._kafka_consumer:
            headers = msg.headers
            if not verify_headers(headers, EXPECTED_HEADERS):
                print("Invalid message headers, skipping message")
                await self._kafka_consumer.commit()
                continue

            order: Order | None = extract_order_from_message(msg.value)
            if order is None:
                print("Failed to extract order from message, skipping message")
                await self._kafka_consumer.commit()
                continue

            await self._prepare_order.prepare_order(order)

            await self._kafka_consumer.commit()
