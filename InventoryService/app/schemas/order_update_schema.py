from uuid import UUID

from pydantic import BaseModel

from InventoryService.app.constants.order_status import OrderStatus


class OrderStatusUpdate(BaseModel):
    order_id: UUID
    status: OrderStatus
