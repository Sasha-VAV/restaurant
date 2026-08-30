from pydantic import BaseModel, Field
from typing import Literal


class Food(BaseModel):
    id: str = Field(
        ...,
        description="The unique identifier for the food item",
        examples=["food_123"],
    )
    name: str = Field(..., description="The name of the food item", examples=["Pizza"])
    price: float = Field(
        ..., description="The price of the food item", examples=[10.99]
    )


class CreateOrderRequest(BaseModel):
    customer_id: str = Field(
        ...,
        description="The unique identifier for the customer",
        examples=["customer_123"],
    )
    items: list[Food] = Field(
        ...,
        description="The list of food items in the order",
        examples=[[Food(id="food_123", name="Pizza", price=10.99)]],
    )


class CreateOrderResponse(BaseModel):
    id: str = Field(
        ..., description="The unique identifier for the order", examples=["order_123"]
    )
    status: Literal["pending", "cancelled"] = Field(
        ..., description="The status of the order", examples=["pending"]
    )
