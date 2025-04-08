from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_pagination import Params

from OrderService.app.core.dependencies import get_redis_client
from OrderService.app.order_management.manager import OrderManager
from OrderService.app.schemas.order_schema import OrderCreate, OrderResponse

router = APIRouter(prefix='/orders')


@router.get('/{order_id}', response_model=OrderResponse,
            description="Retrieve details of a specific order using order ID and user ID.")
async def action(order_id: UUID, user_id: UUID, inventory_cache=Depends(get_redis_client)):
    manager = OrderManager(inventory_cache)
    return await manager.fetch_order(user_id=user_id, order_id=order_id)


@router.get('', response_model=List[OrderResponse],
            description="Get a paginated list of all orders associated with a specific user.")
async def action(user_id: UUID, inventory_cache=Depends(get_redis_client),
                 params: Params = Depends()):
    manager = OrderManager(inventory_cache)
    return await manager.fetch_all_orders(user_id=user_id, params=params)


@router.post('/place_order', response_model=OrderResponse,
             description="Create a new order with the provided order details.")
async def action(order: OrderCreate, inventory_cache=Depends(get_redis_client)):
    manager = OrderManager(inventory_cache)
    return await manager.place_order(order)


@router.patch('/cancel_order', description="Cancel an existing order by providing the order ID and user ID.")
async def action(order_id: UUID, user_id: UUID, inventory_cache=Depends(get_redis_client)):
    manager = OrderManager(inventory_cache)
    await manager.cancel_order(order_id=order_id, user_id=user_id)
