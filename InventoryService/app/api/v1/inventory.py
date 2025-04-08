from typing import List

from fastapi import APIRouter

from InventoryService.app.core.inventory_handler import InventoryHandler
from InventoryService.app.db.models.inventory import Item
from InventoryService.app.schemas.inventory_schema import ItemCreate, ItemUpdate

router = APIRouter(prefix='/inventory')


@router.get('/all_items', response_model=List[Item],
            description="Api endpoint to list all the available items of a store")
async def action(store_id: str):
    return await InventoryHandler().fetch_items(store_id)


@router.post('/add_item', description="Api endpoint for store owners to add items to inventory")
async def action(create_item: ItemCreate):
    return await InventoryHandler().add_new_item(create_item)


@router.patch('/update_item',
              description="Api endpoint for store owners to update items quantity, threshold, price to inventory")
async def action(update_item: ItemUpdate):
    return await InventoryHandler().update_item(update_item)
