from typing import List
from uuid import UUID

from pydantic import BaseModel, PositiveInt


class OrderItemsCreate:
    item_id: UUID
    quantity: PositiveInt


class OrderCreate(BaseModel):
    items: List[OrderItemsCreate]
    user_id: UUID
