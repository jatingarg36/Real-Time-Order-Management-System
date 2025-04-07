import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter

from InventoryService.app.db.crud import add_item, fetch_all_item
from InventoryService.app.db.models.inventory import Item
from InventoryService.app.schemas.inventory_schema import ItemCreate, ItemUpdate

router = APIRouter(prefix='/inventory')


@router.get('/all_items', response_model=List[Item],
            description="Api endpoint to list all the available items of a store")
async def action(store_id: str):
    return await fetch_all_item.action(store_id)


@router.post('/add_items', description="Api endpoint for store owners to add items to inventory")
async def action(create_item: ItemCreate):
    return await add_item.action(Item(**create_item.dict(), item_id=uuid.uuid4(), updated_at=datetime.utcnow()))


@router.patch('/update_item',
              description="Api endpoint for store owners to update items quantity, threshold, price to inventory")
async def action(update_item: ItemUpdate):
    pass
