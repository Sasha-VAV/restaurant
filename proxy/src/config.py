from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = "localhost:9092"
    orders_topic: str = "orders.created"


class AppSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()
    app: AppSettings = AppSettings()
