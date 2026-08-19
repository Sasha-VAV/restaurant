from src.api.schemas import Food as FoodSchema
from src.domain import Food as FoodEntity


def from_food_schema_to_entity(food_schema: FoodSchema) -> FoodEntity:
    return FoodEntity(
        id=food_schema.id,
        name=food_schema.name,
        price=food_schema.price,
    )
