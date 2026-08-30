from fastapi import FastAPI

from src.application.use_cases import CreateOrder
from src.api.routers import orders


def create_app(create_order: CreateOrder) -> FastAPI:
    app = FastAPI()
    app.state.create_order = create_order
    app.include_router(orders.router)
    return app
