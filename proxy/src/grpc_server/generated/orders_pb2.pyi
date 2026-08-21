from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Food(_message.Message):
    __slots__ = ("id", "name", "price")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    price: int
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., price: _Optional[int] = ...) -> None: ...

class CreateOrderRequest(_message.Message):
    __slots__ = ("customer_id", "items")
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    items: _containers.RepeatedCompositeFieldContainer[Food]
    def __init__(self, customer_id: _Optional[str] = ..., items: _Optional[_Iterable[_Union[Food, _Mapping]]] = ...) -> None: ...

class CreateOrderResponse(_message.Message):
    __slots__ = ("order_id",)
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    def __init__(self, order_id: _Optional[str] = ...) -> None: ...

class OrderReadyNotification(_message.Message):
    __slots__ = ("order_id", "tray_id")
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    TRAY_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    tray_id: str
    def __init__(self, order_id: _Optional[str] = ..., tray_id: _Optional[str] = ...) -> None: ...

class OrderStreamChunk(_message.Message):
    __slots__ = ("customer_id", "food")
    CUSTOMER_ID_FIELD_NUMBER: _ClassVar[int]
    FOOD_FIELD_NUMBER: _ClassVar[int]
    customer_id: str
    food: Food
    def __init__(self, customer_id: _Optional[str] = ..., food: _Optional[_Union[Food, _Mapping]] = ...) -> None: ...
