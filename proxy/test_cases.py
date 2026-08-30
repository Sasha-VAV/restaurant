"""This file is used for testing purposes only.
It may violate coding standards and is not intended for production use"""

import asyncio

import grpc
import pytest
from google.protobuf import empty_pb2

from src.grpc_server.generated import orders_pb2, orders_pb2_grpc


async def unary_test_case(stub: orders_pb2_grpc.OrderServiceStub):
    request = orders_pb2.CreateOrderRequest(
        customer_id="c1",
        items=[
            orders_pb2.Food(id="f1", name="Burger", price=999),
            orders_pb2.Food(id="f2", name="Fries", price=299),
        ],
    )
    response = await stub.CreateOrder(request)
    print(f"Created order: {response.order_id}")
    assert response.order_id is not None


async def unary_error_test_case(stub: orders_pb2_grpc.OrderServiceStub):
    request = orders_pb2.CreateOrderRequest()
    with pytest.raises(grpc.aio.AioRpcError) as exc_info:
        await stub.CreateOrder(request)

    print(f"Error code: {exc_info.value.code()}")
    print(f"Error details: {exc_info.value.details()}")


async def client_streaming_test_case(stub: orders_pb2_grpc.OrderServiceStub):
    async def chunk_generator():
        yield orders_pb2.OrderStreamChunk(customer_id="c1")
        yield orders_pb2.OrderStreamChunk(
            food=orders_pb2.Food(id="f1", name="Burger", price=999)
        )
        yield orders_pb2.OrderStreamChunk(
            food=orders_pb2.Food(id="f2", name="Fries", price=299)
        )

    response = await stub.CreateOrderStream(chunk_generator())
    print(f"Created order: {response.order_id}")
    assert response.order_id is not None


async def server_streaming_test_case(stub: orders_pb2_grpc.OrderServiceStub):
    checks = 3
    for _ in range(checks):
        await unary_test_case(stub)

    async for notification in stub.StreamReadyOrders(empty_pb2.Empty()):
        print(f"Order ready: {notification.order_id}, Tray ID: {notification.tray_id}")
        assert notification.order_id is not None
        checks -= 1
        if checks <= 0:
            break


async def bidirectional_streaming_test_case(stub: orders_pb2_grpc.OrderServiceStub):
    async def chunk_generator():
        yield orders_pb2.OrderStreamChunk(customer_id="c1")
        yield orders_pb2.OrderStreamChunk(
            food=orders_pb2.Food(id="f1", name="Burger", price=999)
        )
        yield orders_pb2.OrderStreamChunk(
            food=orders_pb2.Food(id="f2", name="Fries", price=299)
        )

    checks = 2
    async for notification in stub.CreateOrdersWithLiveTray(chunk_generator()):
        print(f"Order ready: {notification.order_id}, Tray ID: {notification.tray_id}")
        assert notification.order_id is not None
        checks -= 1
        if checks <= 0:
            break


async def main():
    async with grpc.aio.insecure_channel("localhost:50051") as channel:
        stub = orders_pb2_grpc.OrderServiceStub(channel)

        # print("Running unary test case...")
        # await unary_test_case(stub)

        print("Running unary error test case...")
        await unary_error_test_case(stub)

        # print("Running client streaming test case...")
        # await client_streaming_test_case(stub)

        # print("Running server streaming test case...")
        # await server_streaming_test_case(stub)

        print("Running bidirectional streaming test case...")
        await bidirectional_streaming_test_case(stub)


if __name__ == "__main__":
    asyncio.run(main())
