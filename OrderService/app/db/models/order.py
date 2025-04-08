from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from OrderService.app.constants.order_status import OrderStatus


class Order(BaseModel):
    order_id: UUID
    status: OrderStatus
    user_id: UUID
    store_id: UUID
    total_amount: float
    payment_id: UUID
    created_at: datetime
    updated_at: datetime


class OrderItems(BaseModel):
    order_id: UUID
    item_id: UUID
    quantity: int


class OrderUpdate(BaseModel):
    order_id: UUID
    status: OrderStatus
    updated_at: datetime
    reason: Optional[str] = None
