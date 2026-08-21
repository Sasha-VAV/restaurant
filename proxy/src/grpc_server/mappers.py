from src.domain import Food
from src.grpc_server.generated import orders_pb2


def food_proto_to_entity(food_proto: orders_pb2.Food) -> Food:
    print(food_proto.price)
    return Food(
        id=food_proto.id,
        name=food_proto.name,
        price=food_proto.price / 100,
    )
