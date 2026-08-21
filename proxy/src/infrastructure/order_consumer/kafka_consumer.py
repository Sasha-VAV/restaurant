import asyncio
import json
from aiokafka import AIOKafkaConsumer
import typing

from src.config import KafkaSettings
from src.application.use_cases.receive_tray import ReceiveTray
from src.domain import FinishedOrder
from src.infrastructure.lifecycle import Startable


IDENTITY_HEADERS = {"event_type": "order.finished", "schema_version": "1"}


def verify_headers(
    headers: typing.Iterable[tuple[str, bytes]], expected_headers: dict[str, str]
) -> bool:
    for key, value in headers:
        if key in expected_headers and value.decode() != expected_headers[key]:
            return False
    return True


def decode_message_value(value: bytes) -> FinishedOrder | None:
    try:
        order = json.loads(value.decode())
        return FinishedOrder(**order)
    except (KeyError, json.JSONDecodeError):
        return None


class KafkaTrayReceiver(Startable):
    def __init__(self, settings: KafkaSettings, receive_tray_use_case: ReceiveTray):
        self._settings = settings
        self._receive_tray_use_case = receive_tray_use_case
        self._consumer: AIOKafkaConsumer | None = None
        self._task: asyncio.Task | None = None

    async def start(self):
        self._consumer = AIOKafkaConsumer(
            self._settings.finished_orders_topic,
            bootstrap_servers=self._settings.bootstrap_servers,
            group_id=self._settings.group_id,
            key_deserializer=lambda k: k,
            value_deserializer=lambda v: v,
            auto_offset_reset="earliest",
            enable_auto_commit=False,
        )
        await self._consumer.start()
        print("Kafka consumer started. Listening for finished orders...")
        self._task = asyncio.create_task(self._process_loop())

    async def stop(self):
        if self._consumer:
            await self._consumer.stop()

    async def _process_loop(self):
        if not self._consumer:
            raise RuntimeError("Consumer is not initialized. Call start() first.")

        async for msg in self._consumer:
            if not verify_headers(msg.headers, IDENTITY_HEADERS):
                print(
                    f"Received message with unexpected headers: {msg.headers}. Skipping."
                )
                await self._consumer.commit()
                continue
            if msg.value is None:
                print("Received message with no value. Skipping.")
                await self._consumer.commit()
                continue
            order = decode_message_value(msg.value)
            if order is None:
                print(f"Failed to decode message value: {msg.value}. Skipping.")
                await self._consumer.commit()
                continue

            await self._receive_tray_use_case.receive_tray(order)

            await self._consumer.commit()
