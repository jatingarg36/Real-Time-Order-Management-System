import uuid
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, constr, Field


class ItemUpdate(BaseModel):
    store_id: UUID
    item_id: UUID
    add_quantity: Optional[int] = 0
    new_price: Optional[int] = None
    new_alert_threshold: Optional[int] = None


class ItemCreate(BaseModel):
    store_id: UUID = uuid.uuid4()
    item_name: constr(max_length=20)
    item_description: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)
    alert_threshold: int = Field(..., ge=0)
