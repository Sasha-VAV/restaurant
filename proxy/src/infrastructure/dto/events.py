from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from uuid import uuid4

from src.domain import Order


@dataclass(frozen=True)
class OrderCreatedEvent:
    payload: Order
    event_type: str
    schema_version: int
    message_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def payload_to_dict(self) -> dict:
        return asdict(self.payload)
