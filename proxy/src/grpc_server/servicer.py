import asyncio
import typing as tp

import grpc
from grpc.aio import ServicerContext
from google.protobuf import empty_pb2

from src.grpc_server.generated import orders_pb2_grpc, orders_pb2
from src.grpc_server.mappers import food_proto_to_entity
from src.application.use_cases import CreateOrder, ReceiveTray
from src.domain import Food


class OrderServicer(orders_pb2_grpc.OrderServiceServicer):
    def __init__(self, create_order: CreateOrder, receive_tray: ReceiveTray):
        self._create_order = create_order
        self._receive_tray = receive_tray

    async def CreateOrder(
        self, request: orders_pb2.CreateOrderRequest, context: ServicerContext
    ) -> orders_pb2.CreateOrderResponse:
        food_items = [food_proto_to_entity(food) for food in request.items]
        order = await self._create_order.create_order(request.customer_id, food_items)
        return orders_pb2.CreateOrderResponse(order_id=order.id)

    async def StreamReadyOrders(
        self, request: empty_pb2.Empty, context: ServicerContext
    ) -> tp.AsyncIterator[orders_pb2.OrderReadyNotification]:
        async for order in self._receive_tray.subscribe():
            yield orders_pb2.OrderReadyNotification(
                order_id=order.id, tray_id=order.tray_id
            )

    async def CreateOrderStream(
        self,
        request_iterator: tp.AsyncIterator[orders_pb2.OrderStreamChunk],
        context: ServicerContext,
    ) -> orders_pb2.CreateOrderResponse:
        customer_id: str | None = None
        food_items: list[Food] = []

        async for chunk in request_iterator:
            which = chunk.WhichOneof("chunk")

            if which == "customer_id":
                if customer_id is not None:
                    await context.abort(
                        grpc.StatusCode.INVALID_ARGUMENT, "Customer ID already set"
                    )
                customer_id = chunk.customer_id
            elif which == "food":
                food_items.append(food_proto_to_entity(chunk.food))
            else:
                await context.abort(
                    grpc.StatusCode.INVALID_ARGUMENT, f"Unknown chunk type: {which}"
                )

        if customer_id is None:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "Customer ID not provided"
            )

        if not food_items:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT, "No food items provided"
            )

        order = await self._create_order.create_order(customer_id, food_items)
        return orders_pb2.CreateOrderResponse(order_id=order.id)

    async def CreateOrdersWithLiveTray(
        self,
        request_iterator: tp.AsyncIterator[orders_pb2.OrderStreamChunk],
        context: ServicerContext,
    ) -> tp.AsyncIterator[orders_pb2.OrderReadyNotification]:
        async def consume_orders():
            customer_id: str | None = None
            async for chunk in request_iterator:
                which = chunk.WhichOneof("chunk")
                if which == "customer_id":
                    if customer_id is not None:
                        customer_id = chunk.customer_id  # We got new customer
                    customer_id = chunk.customer_id
                elif which == "food":
                    if customer_id is None:
                        await context.abort(
                            grpc.StatusCode.INVALID_ARGUMENT,
                            "Customer ID not provided before food items",
                        )
                    await self._create_order.create_order(
                        customer_id, [food_proto_to_entity(chunk.food)]
                    )
                else:
                    await context.abort(
                        grpc.StatusCode.INVALID_ARGUMENT, f"Unknown chunk type: {which}"
                    )

        consume_task = asyncio.create_task(consume_orders())

        try:
            async for finished_order in self._receive_tray.subscribe():
                yield orders_pb2.OrderReadyNotification(
                    order_id=finished_order.id, tray_id=finished_order.tray_id
                )
        finally:
            consume_task.cancel()
            try:
                await consume_task
            except asyncio.CancelledError:
                pass
