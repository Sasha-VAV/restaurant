from fastapi import Request
from src.application.use_cases import CreateOrder


def get_create_order_use_case(request: Request) -> CreateOrder:
    return CreateOrder(order_publisher=request.app.state.order_publisher)
