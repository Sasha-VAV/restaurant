from src.application.ports import OrderPublisher
from src.domain import Order
from src.infrastructure.lifecycle import Startable


class KafkaOrderPublisher(OrderPublisher, Startable):
    async def start(self):
        # TODO implement the logic to start the Kafka producer
        pass

    async def publish(self, order: Order):
        # TODO implement the logic to publish the order to Kafka
        pass

    async def stop(self):
        # TODO implement the logic to stop the Kafka producer
        pass
