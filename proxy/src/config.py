from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = "localhost:9092"
    group_id: str = "proxy-service"
    created_orders_topic: str = "orders.created"
    finished_orders_topic: str = "orders.finished"


class FastAPISettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


class GRPCSettings(BaseSettings):
    port: int = 50051


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()
    fastapi: FastAPISettings = FastAPISettings()
    grpc: GRPCSettings = GRPCSettings()
