from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, PositiveInt

from OrderService.app.constants.order_status import OrderStatus


class OrderItemsCreate(BaseModel):
    item_id: UUID
    quantity: PositiveInt


class OrderCreate(BaseModel):
    items: List[OrderItemsCreate]
    user_id: UUID
    total_price: float
    store_id: UUID


class OrderItemResponse(BaseModel):
    item_id: UUID
    item_name: str
    quantity: int


class OrderResponse(BaseModel):
    order_id: UUID
    status: OrderStatus
    user_id: UUID
    store_id: UUID
    total_amount: float
    payment_id: UUID
    items: List[OrderItemResponse]
    created_at: datetime
    updated_at: datetime
