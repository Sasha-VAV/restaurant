import grpc
from src.grpc_server.servicer import OrderServicer
from src.grpc_server.generated import orders_pb2_grpc
from src.infrastructure.lifecycle import Startable
from src.application.use_cases import CreateOrder, ReceiveTray


class GRPCServer(Startable):
    def __init__(self, create_order: CreateOrder, receive_tray: ReceiveTray, port: int):
        self._port = port
        self._servicer = OrderServicer(create_order, receive_tray)
        self._server: grpc.aio.Server | None = None

    async def start(self):
        self._server = grpc.aio.server()
        orders_pb2_grpc.add_OrderServiceServicer_to_server(self._servicer, self._server)
        self._server.add_insecure_port(f"[::]:{self._port}")
        await self._server.start()
        print("gRPC server started. Listening for requests...")

    async def stop(self):
        if self._server:
            await self._server.stop(grace=5)
