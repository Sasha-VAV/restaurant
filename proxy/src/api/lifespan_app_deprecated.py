from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.config import Settings
from src.infrastructure.order_publisher.kafka_publisher import KafkaOrderPublisher
from src.api.routers import orders


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = app.state.settings

    publisher = KafkaOrderPublisher(settings=settings.kafka)
    await publisher.start()

    app.state.order_publisher = publisher

    yield

    await publisher.stop()


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.state.settings = settings
    app.include_router(orders.router)
    return app
