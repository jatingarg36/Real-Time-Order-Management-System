from fastapi import APIRouter

from InventoryService.app.core.order_status_handler import OrderStatusHandler
from InventoryService.app.schemas.order_update_schema import OrderStatusUpdate

router = APIRouter(prefix='/orders')


@router.patch('/update_status', response_model=bool, description="Api endpoint update the status of am order")
async def action(order_update: OrderStatusUpdate):
    result = await OrderStatusHandler(order_update).update()
    return result
