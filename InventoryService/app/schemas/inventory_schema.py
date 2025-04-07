import uuid
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ItemUpdate(BaseModel):
    store_id: UUID
    item_id: UUID
    add_quantity: Optional[int] = 0
    new_price: Optional[int] = None
    new_alert_threshold: Optional[int] = None


class ItemCreate(BaseModel):
    store_id: UUID = uuid.uuid4()
    item_name: str
    item_description: str
    price: float
    quantity: int
    alert_threshold: int

