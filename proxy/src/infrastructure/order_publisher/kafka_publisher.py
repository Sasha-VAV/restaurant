import json

from aiokafka import AIOKafkaProducer


from src.application.ports import OrderPublisher
from src.domain import Order
from src.infrastructure.lifecycle import Startable
from src.infrastructure.dto.events import OrderCreatedEvent
from src.config import KafkaSettings


class KafkaOrderPublisher(OrderPublisher, Startable):
    def __init__(self, settings: KafkaSettings):
        self._settings = settings
        self._producer: AIOKafkaProducer | None = None

    async def start(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._settings.bootstrap_servers,
            # API LOGIC
            key_serializer=lambda k: k.encode("utf-8"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            # KAFKA POLICY
            acks="all",
            enable_idempotence=True,
        )

        await self._producer.start()

    async def publish(self, order: Order):
        created_event = OrderCreatedEvent(
            payload=order,
            event_type="order.created",
            schema_version=1,
        )
        await self._publish(created_event)

    async def _publish(self, event: OrderCreatedEvent):
        if not self._producer:
            raise RuntimeError(
                "Kafka producer is not started. Call start() before publishing."
            )

        await self._producer.send_and_wait(
            topic=self._settings.orders_topic,
            key=event.message_id,
            value=event.payload_to_dict(),
            headers=[
                ("event_type", event.event_type.encode("utf-8")),
                ("schema_version", str(event.schema_version).encode("utf-8")),
            ],
        )

    async def stop(self):
        if self._producer:
            await self._producer.stop()
