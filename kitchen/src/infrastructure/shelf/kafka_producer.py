import json

from aiokafka import AIOKafkaProducer

from src.config import KafkaSettings
from src.application.ports.shelf import Shelf
from src.domain.entities.order import FinishedOrder
from src.infrastructure.lifecycle import Startable


IDENTITY_HEADERS = [
    ("event_type", b"order.finished"),
    ("schema_version", b"1"),
]


class ShelfKafkaProducer(Shelf, Startable):
    def __init__(self, settings: KafkaSettings):
        self._settings = settings
        self._kafka_producer: AIOKafkaProducer | None = None

    async def start(self):
        self._kafka_producer = AIOKafkaProducer(
            bootstrap_servers=self._settings.bootstrap_servers,
            key_serializer=lambda k: k.encode("utf-8"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all",
            enable_idempotence=True,
        )
        await self._kafka_producer.start()
        print(
            f"Kafka producer started with bootstrap servers: {self._settings.bootstrap_servers}"
        )

    async def stop(self):
        if self._kafka_producer is not None:
            await self._kafka_producer.stop()

    async def add_order(self, order: FinishedOrder) -> None:
        if self._kafka_producer is None:
            raise RuntimeError("Kafka producer is not started")

        await self._kafka_producer.send(
            topic=self._settings.order_finished_topic,
            key=order.id,
            value=order.to_dict(),
            headers=IDENTITY_HEADERS,
        )
