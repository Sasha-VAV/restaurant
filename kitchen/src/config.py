from pydantic_settings import BaseSettings


class KafkaSettings(BaseSettings):
    bootstrap_servers: str = "localhost:9092"
    group_id: str = "kitchen-service"
    order_created_topic: str = "orders.created"
    order_finished_topic: str = "orders.finished"


class Settings(BaseSettings):
    kafka: KafkaSettings = KafkaSettings()
