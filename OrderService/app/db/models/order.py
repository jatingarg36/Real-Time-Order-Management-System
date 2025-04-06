from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class Order(BaseModel):
    order_id: UUID
    status: str
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
