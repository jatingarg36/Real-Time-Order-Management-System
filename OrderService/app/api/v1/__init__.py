from fastapi import APIRouter

from OrderService.app.api.v1.orders import router as order_router

router = APIRouter(prefix='/api/v1')

router.include_router(order_router)
