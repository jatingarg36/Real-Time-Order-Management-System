from fastapi import APIRouter

from InventoryService.app.api.v1.inventory import router as inventory_router
from InventoryService.app.api.v1.order import router as order_router

router = APIRouter(prefix='/api/v1')

router.include_router(inventory_router)
router.include_router(order_router)
