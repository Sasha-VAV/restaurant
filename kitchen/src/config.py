from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = "localhost:9092"
    group_id: str = "kitchen-service"
    topic: str = "orders.created"


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()
