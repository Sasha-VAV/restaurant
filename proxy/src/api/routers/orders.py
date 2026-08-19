from fastapi import Depends, APIRouter

from src.api.schemas.order import CreateOrderRequest, CreateOrderResponse
from src.api.dependencies import get_create_order_use_case
from src.api.mappers import from_food_schema_to_entity
from src.application.use_cases import CreateOrder

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=CreateOrderResponse, status_code=202)
async def create_order(
    payload: CreateOrderRequest,
    create_order_use_case: CreateOrder = Depends(get_create_order_use_case),
):
    order = await create_order_use_case.create_order(
        customer_id=payload.customer_id,
        food_items=[from_food_schema_to_entity(item) for item in payload.items],
    )
    return CreateOrderResponse(id=order.id, status="pending")
