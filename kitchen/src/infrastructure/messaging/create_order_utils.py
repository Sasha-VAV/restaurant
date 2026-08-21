import json
from src.domain.entities.order import Order, Food


def verify_headers(headers: list[tuple[str, bytes]], expected: dict[str, str]) -> bool:
    for key, value in headers:
        if key not in expected or value.decode() != expected[key]:
            return False
    return True


def extract_order_from_message(message: bytes) -> Order | None:
    try:
        order_data = json.loads(message.decode())
    except json.JSONDecodeError as e:
        print(f"Error decoding message: {e}")
        return None
    try:
        order = Order(
            id=order_data["id"],
            customer_id=order_data["customer_id"],
            items=[
                Food(id=item["id"], name=item["name"], price=item["price"])
                for item in order_data["items"]
            ],
        )
    except KeyError as e:
        print(f"Missing key in order data: {e}")
        return None
    return order
