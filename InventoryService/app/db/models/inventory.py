from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Item(BaseModel):
    store_id: UUID = Field(..., description="Store associated with the item",
                           examples=["011ae52d-929f-44a7-af32-6141dcd14f0d"])
    item_id: UUID = Field(..., description="Unique identifier for the item",
                          examples=["123e4567-e89b-12d3-a456-426614174000"])
    item_name: str = Field(..., min_length=1, max_length=20, description="Name of the item", examples=["Cheeseburger"])
    item_description: str = Field(..., min_length=1, max_length=500, description="Detailed description of the item",
                                  examples=["A juicy cheeseburger with lettuce and tomato."])
    price: float = Field(..., gt=0, description="Price of the item in USD", examples=[9.99])
    quantity: int = Field(..., ge=0, description="Available stock quantity", examples=[50])
    alert_threshold: int = Field(..., ge=0, description="Threshold to trigger low stock alert", examples=[10])
    updated_at: datetime = Field(..., description="Timestamp when the item was last updated",
                                 examples=["2023-12-31T23:59:59Z"])

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "store_id": "011ae52d-929f-44a7-af32-6141dcd14f0d",
                "item_id": "123e4567-e89b-12d3-a456-426614174000",
                "item_name": "Cheeseburger",
                "item_description": "A juicy cheeseburger with lettuce and tomato.",
                "price": 9.99,
                "quantity": 50,
                "alert_threshold": 10,
                "updated_at": "2023-12-31T23:59:59Z"
            }
        }
    }
