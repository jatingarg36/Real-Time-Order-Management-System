from fastapi import APIRouter

from OrderService.app.schemas.order_schema import OrderCreate

router = APIRouter(prefix='/orders')

@router.get('/{user_id}', description='list all the orders for a user')
async def action(user_id: str):
    pass

@router.post('/place_order', description="Api endpoint to create an order")
async def action(order: OrderCreate):
    pass